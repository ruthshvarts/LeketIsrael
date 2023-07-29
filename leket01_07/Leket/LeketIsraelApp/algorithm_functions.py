import pandas as pd
import pandasql as ps
from LeketIsraelApp.models import leket_DB
import datetime
import matplotlib.pyplot as plt
import io
import base64
import pickle


def find_keys_by_value(dictionary, search_value):
    # Using a list comprehension to find all keys that match the search_value
    found_keys = [key for key, values in dictionary.items() if search_value in values]
    return found_keys

def create_area_dict(df):
    area_dict = {}
    for index, row in df.iterrows():
        area = row['area']
        napa_name = row['napa_name']

        if area in area_dict:
            area_dict[area].add(napa_name)
        else:
            area_dict[area] = {napa_name}
        area_dict.keys()
    return area_dict

def create_napa_dict(df):
    result_dict = {}
    for index, row in df.iterrows():
        area = row['napa_name']
        location = row['leket_location']

        # Check if the area is already a key in the dictionary
        if area in result_dict:
            # Add the location to the set of locations for the area
            result_dict[area].add(location)
        else:
            # Create a new set with the location and assign it to the area key
            result_dict[area] = {location}
    # Print the resulting dictionary
    result_dict.keys()
    return result_dict


def openfile(file, column1,column2, value):
    df = pd.read_csv(file, encoding='utf-8-sig')
    if value not in df[column1].values: return -1
    val = df[df[column1] == value]
    return val[column2].values[0]


def load_model_from_pickle(filename):
    try:
        with open(filename, 'rb') as file:
            model = pickle.load(file)
        return model
    except Exception as e:
        print(f"Error occurred while loading the model: {str(e)}")
        return None


def run(end_date, location, chag, type,napa_name):
    loaded_model = load_model_from_pickle('random_forest_model.pkl')

    all_records = leket_DB.objects.all()
    # Retrieve the values from the queryset
    record_values = all_records.values()
    # Convert the values to a pandas DataFrame
    df = pd.DataFrame.from_records(record_values)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['week'] = df['date'].dt.isocalendar().week
    df['ground_temp'] = pd.to_numeric(df['ground_temp'], errors='coerce')
    chag_val = (1 if chag == "כן" else 0)
    end_date1 = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    end_year = end_date1.year
    end_month = end_date1.month
    end_week = end_date1.isocalendar()[1]

    # shmita year calculation is in a website i found, and gpt gave a way to calculate it
    shmita_val = (1 if ((end_year + 3760) % 7) == 0 else 0)

    q1 = """
    SELECT
        count (distinct missionID) as num_of_orders,
        year,
        month,
        week,
        area,
        leket_location,
        type,
        napa_name,
        aklim_area,
        TMY_station,
        station,
        ground_temp,
        shmita,
        chagim,
        sum(amount_kg) as sum_amount_kg
    FROM df
    GROUP BY 2,3,4,5,6,7,8,9,10,11,12,13,14
    """
    df = ps.sqldf(q1, locals())

    napa_dict = create_napa_dict(df)
    area_dict = create_area_dict(df)
    area = find_keys_by_value(area_dict,napa_name)
    print(area)
    print(napa_name)
    print(area_dict)
    encoded_area = openfile('areas_oncoding.csv', 'original_area', 'area', area[0])
    if df.empty:
        return (df, shmita_val)
    x = napa_dict[napa_name]
    encoded_type = openfile('types_oncoding.csv','original_type', 'type', type)

    test = []
    leket_location_arr = []
    for i in x:
        encoded_location = openfile('leket_locations_oncoding.csv', 'original_leket_location',
                                    'leket_location', i)
        if encoded_location == -1: continue
        leket_location_arr.append(i)

        test.append([1,end_year,end_month,end_week,encoded_area,encoded_location,encoded_type,shmita_val,chag_val])
    test_df = pd.DataFrame(test, columns=['num_of_orders', 'year', 'month','week','area','leket_location',
                                          'type','shmita','chagim'])
    test_preds = loaded_model.predict(test_df)

    leket_location_prediction = pd.DataFrame({'leket_location': leket_location_arr, 'test_preds': test_preds})
    leket_location_prediction['test_preds'] = test_preds.round()
    leket_location_prediction = leket_location_prediction.sort_values('test_preds', ascending=False)

    return (df, shmita_val, leket_location_prediction, leket_location_arr)


def create_an_image(leket_location ,type ,chag, end_date, location_pred):
    all_records = leket_DB.objects.all()
    record_values = all_records.values()
    df = pd.DataFrame.from_records(record_values)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['week'] = df['date'].dt.isocalendar().week

    end_date1 = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    end_year = end_date1.year
    end_month = end_date1.month
    end_week = end_date1.isocalendar()[1]
    chag_val = (1 if chag == "כן" else 0)

    q1 = """
        SELECT *
        FROM df
        WHERE year BETWEEN {0} AND {1}
              AND week = {2} and leket_location='{3}' and [type] ='{4}' AND chagim = {5}
        """.format(end_year - 3, end_year, end_week, leket_location, type, chag_val)
    df = ps.sqldf(q1, locals())

    if df.empty:
        location_image_base64 = "message"
        farmers_mean_image_base64 = "message"
        fig, ax = plt.subplots()
        ax.axis('off')
        # Add the text to the axis
        ax.text(0.5, 0.5, "רבע ינותנ ןיא",
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=32,
                fontweight='bold',
                fontname='Tahoma')

        # Save the figure as an image
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', facecolor='none')
        buffer.seek(0)
        message_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()

    else:
        message_base64 = 'There is data'
        farmers_mean = df.groupby(['year', 'farmerID'])['amount_kg'].mean().round().astype(int)
        farmers_mean = farmers_mean.fillna(0)
        farmers_mean = pd.DataFrame(farmers_mean)
        farmers_mean.reset_index(inplace=True)
        farmers_mean = farmers_mean.pivot(index='farmerID', columns='year', values='amount_kg').fillna(0)
        print(farmers_mean)
        # display bar plot
        plt.figure(facecolor='none')
        grouped = df.groupby('year')['amount_kg'].mean()
        grouped = pd.DataFrame(grouped)
        grouped.reset_index(inplace=True)
        # new_row data
        new_row = {'year': int(end_year), 'amount_kg': location_pred}
        # Create a DataFrame with new_row data and preserve the index column
        new_row_df = pd.DataFrame(new_row, index=[0], columns=['year', 'amount_kg'])
        # Concatenate the new row DataFrame with the original DataFrame, preserving the index column
        grouped = pd.concat([grouped, new_row_df], ignore_index=True)
        grouped['amount_kg'] = pd.to_numeric(grouped['amount_kg'])
        # Define the colors for the bars
        color_existing = '#f6a172'  # Color for existing records
        color_new = '#7cb6e8'  # Color for the new record

        # Create the horizontal bar plot
        ax = grouped.plot(kind='barh', x='year', y='amount_kg', color=color_existing)

        # Get the index of the new record
        new_record_index = grouped.index[-1]

        # Set the color of the new record bar
        ax.patches[new_record_index].set_color(color_new)
        # Customize the plot appearance
        ax.set_facecolor('lightgray')  # Set the background color of the plot area
        ax.spines['top'].set_visible(False)  # Hide the top border
        ax.spines['right'].set_visible(False)  # Hide the right border
        ax.set_xlabel('ג"קב תעצמומ תומכ',fontname='Tahoma')
        ax.set_ylabel('הנש',fontname='Tahoma')
        ax.set_facecolor('none')
        # ax.set_title('{} לש עובשה רובע ג"קב תעצמומ תומכ'.format(end_date))
        plt.suptitle("{} לש עובשה רובע תעצמומ תומכ\n לוחכ עבצב ןמוסמ יוזיחה".format(end_date), fontname='Tahoma', fontsize=14)
        ax.legend().remove()
        plt.tight_layout() # Adjust the layout and spacing

        for rect in ax.patches:
            width = rect.get_width()
            height = rect.get_height()
            x = rect.get_x()
            y = rect.get_y()

            ax.annotate(f'{width:.1f}', xy=(x + width / 2, y + height / 2),
                        xytext=(0, 0), textcoords='offset points',
                        ha='center', va='center')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', facecolor='none')
        buffer.seek(0)
        location_image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()

        # Saving farmers_mean DataFrame as an image
        fig2, ax2 = plt.subplots(figsize=(8, 4))  # Adjust the figure size as needed
        ax2.axis('off')
        table = ax2.table(cellText=farmers_mean.values,
                          colLabels=farmers_mean.columns,
                          rowLabels=farmers_mean.index,
                          loc='center',
                          cellLoc='center',
                          cellColours=[['lightgray']*len(farmers_mean.columns)]*len(farmers_mean),
                          colWidths=[0.08]*len(farmers_mean.columns),
                          bbox=[0, 0, 0.6, 0.6])

        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(0.5, 0.5)

        for cell in table._cells:
            table._cells[cell].set_facecolor('none')

        for key, cell in table.get_celld().items():
            if key[0] == 0:  # Header row
                cell.set_text_props(weight='bold')

        title_text = 'יאלקח יפל תעצוממ תומכ'
        title_bbox = {'boxstyle': 'round', 'facecolor': 'wheat', 'alpha': 1}
        title = ax2.set_title(title_text, fontsize=14, fontname='Tahoma' , y=0.7,x=0.3)
        # Save the table as an image
        buffer2 = io.BytesIO()
        plt.savefig(buffer2, format='png', bbox_inches='tight', transparent=True, pad_inches=0.1)
        buffer2.seek(0)
        farmers_mean_image_base64 = base64.b64encode(buffer2.read()).decode('utf-8')
        buffer2.close()

    return location_image_base64, farmers_mean_image_base64, message_base64
