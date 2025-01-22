import dash
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import sys
import sqlite3
import dash_bootstrap_components as dbc
from datetime import datetime
from dash import dash_table
import numpy as np

# Data for the table with additional columns

pd.set_option('display.max_columns', None)

data_try = pd.DataFrame()

global Manager_selections

d = data_try.copy()
selections_checklist = []
Manager_selections = {}
data_try_temp_2 = data_try_temp = data_try.copy()

# Jarir_Logo = Image.open("C:/Users/ASUS/Downloads/Jarir.jpg")

img  = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWHjsqRBr2Z1x1CPKLmZw54AcooJFpKyGGDA&s'

Login_Layout = html.Div([

    html.Div([

        html.Img(
            src=img,
            style={'width': '600px', 'height': '450px', 'border-radius': '190px 190px 190px', 'marginLeft': '140px',
                   'marginTop': '125px', 'display': 'flex'},
            id='jarirlogo')

    ]),

    html.Div([
        html.H1('LOGIN PAGE',
                style={'font-family': 'Algerian', 'text-align': 'center', 'marginTop': '25px', 'color': '#036073'}),

        dcc.Input(
            id='Username',
            # options=Teritory,
            # value=[],
            # multi=True,
            style={'background-color': '#d8f8ff', 'width': '500px', 'padding': '28px', 'borderRadius': '50px',
                   'margin-left': '70px', 'marginTop': '35px', 'border': '0.5px solid #036073', 'boxShadow': 'none'},
            placeholder='Enter Your Username'
        ),

        dcc.Input(
            id='Password',
            # options=Teritory,4
            # value=[],
            # multi=True,
            type='password',
            style={'background-color': '#d8f8ff', 'width': '500px', 'padding': '28px', 'borderRadius': '50px',
                   'margin-left': '70px', 'marginTop': '55px', 'border': '0.5px solid #036073', 'boxShadow': 'none'},
            placeholder='Enter Your Password'
        ),

        dbc.Button("Submit", id="Submit_Login", n_clicks=0, outline=True, color="primary", className="me-1",
                   style={'padding': '20px', 'width': '320px', 'margin-top': '85px',
                          "font-size": "30px", "font-weight": "bold", 'font-family': 'algerian',
                          'borderRadius': '120px', 'margin-left': '170px'}),

        html.Div(id='Login_Output')

    ], style={'background-color': '#d8f8ff', 'border': '1px solid #0091af', 'border-radius': '20px',
              'marginTop': '90px', 'marginLeft': '100px', 'height': '650px', 'width': '650px'})

], style={'background-color': 'F5FEFF', 'height': '100vh', 'width': '100vw', 'display': 'flex'})
# ] , style={'background-color':'#d8f8ff', 'height':'100vh', 'width':'100vw', 'display':'flex' })


# CSS styles for the table and cells
table_container_style = {
    'overflow-x': 'auto',
    'overflow-y': 'auto',
    'max-height': '900px',
    'width': '173%',
    'border': '1px solid black',
    'border-radius': '4px',
    'margin': '-100px auto',
    'margin-left': '-470px',
    # 'margin-top':'10px'
}


striped_row_style = {
    'background-color': '#f2f2f2'
}

VALID_USERNAME = None

data = pd.read_excel('assets/Vendor_Details.xlsx')
data = data.fillna('NULLVALUES')
# data['Vendor'] = data['Vendor'].astype('int')

data.loc[len(data)] = 'SELECT_ALL'


data['VendorPrefix'] = data['VendorPrefix'].apply(lambda x: str(x).split()[0])

# this sorting is done to show the SELECT_ALL values always on the top
Supplier_Name = sorted(list(set(data['VendorPrefixWithoutCode'])), key=lambda x: (
    isinstance(x, str), x), reverse=True)
Supplier_Number = sorted(list(set(data['Vendor'])), key=lambda x: (
    isinstance(x, str), x), reverse=True)
vendor_prefix = sorted(list(set(data['VendorPrefix'])), key=lambda x: (
    isinstance(x, str), x), reverse=True)
GLCLASS = sorted(list(set(data['GLClass'])), key=lambda x: (
    isinstance(x, str), x), reverse=True)
Classification = sorted(list(set(data['ClassificationDescription1'])), key=lambda x: (
    isinstance(x, str), x), reverse=True)
Model = sorted(list(set(data['Model'])), key=lambda x: (
    isinstance(x, str), x), reverse=True)

# Renaming the columns friendly so that you can understand the columns by their name easily in the callbacks.
old_names = data.columns.to_list()
new_names_Vendor = ['Supplier_Name', 'Supplier_Number',
                    'Vendor_Prefix', 'GLCLASS', 'Classification', 'Model']
rename_dict = dict(zip(old_names, new_names_Vendor))
data = data.rename(columns=rename_dict)

# Variables for Selecion Criteria for Vendor Dropdowns
Vendor_selection = {'Vendor Supplier_Name': None, 'Vendor Supplier_Number': None, 'Vendor Vendor_Prefix': None,
                    'Vendor GLCLASS': None, 'Vendor Classification': None, 'Vendor Model': None, 'Rebate Rebate_Teritory': None,
                    'Rebate Rebate_Period_From': None, 'Rebate Rebate_Period_TO': None, 'Rebate Rebate_Frequency': None,
                    'Rebate Rebate_Currency': None, 'Rebate Rebate_Type': None, 'InputSalesAmount': None,  'InputRebatesMargin': None
                    }

Vendor_Seq_List = []
# Vendor_Seq_List = ['Vendor Supplier_Name', 'Vendor Supplier_Number', 'Vendor Vendor_Prefix', 'Vendor GLCLASS', 'Vendor Classification',
#                    'Vendor Model']

Vendor_Var = 0

# for randome Selections for vendor dropdwons
filtered_data = data.copy()

data2 = pd.read_excel('assets/Rebate_Master.xlsx')

data2 = data2[['Teritory', 'Rebate From Date', 'Rebate To Date',
               'Rebate Frequency', 'Currency', 'Rebate Type']]

Current_Year_Dates = pd.date_range(datetime(datetime.now().year, 1, 1), datetime.now()).strftime('%d-%b-%Y').tolist()

Teritory = sorted(list(set(data2['Teritory'])), key=lambda x: (isinstance(x, str), x), reverse=True)

Rebate_Period_From = Current_Year_Dates
Rebate_Period_TO = Current_Year_Dates

Rebate_Frequency = sorted(list(set(data2['Rebate Frequency'])), key=lambda x: (isinstance(x, str), x), reverse=True)
Rebate_Currency = sorted(list(set(data2['Currency'])), key=lambda x: (isinstance(x, str), x), reverse=True)
Rebate_Type = sorted(list(set(data2['Rebate Type'])), key=lambda x: (isinstance(x, str), x), reverse=True)

Teritory_Currency = ['Bahrain', 'BHD', 'UAE', 'AED', 'Qatar', 'QAR', 'USA', 'USD', 'UK' , 'Pounds', 'Japan', 'JPY',
                     'Kuwait', 'KWD', 'KSA', 'SAR', 'EUROPE', 'EUR', 'EGYPT', 'EGP']

# Teritory_Currency = pd.DataFrame({
#                                     'Teritory': ['United States', 'KSA' ,'UAE','QATAR', 'KUWAIT', 'EUROPE','EGYPT'],
#                                     'Currency': ['USD', 'UAE', 'AED', 'QAR', 'KWD', 'EUR' ,'EGP']
# })


# Renaming the columns friendly so that you can understand the columns by their name easily in the callbacks.
old_names = data2.columns.to_list()

new_names_Rebate = ['Rebate_Teritory', 'Rebate_Period_From',
                    'Rebate_Period_TO', 'Rebate_Frequency', 'Rebate_Currency', 'Rebate_Type']
rename_dict = dict(zip(old_names, new_names_Rebate))
data2 = data2.rename(columns=rename_dict)


Slabs = ['0 - 1,000,000 SAR', '1,000,000-3,000,000 SAR',
         '3,000,000-6,000,000 SAR', '6,000,000-10,000,000 SAR', '10000000 SAR and Above']
Rebates = [str(round(i*0.1, 1))+' %' for i in range(1, 82)]


app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server 

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    dcc.Location(id='url2', refresh=True),
    dcc.Location(id='url3', refresh=True),
    dcc.Store(id='selected-values', storage_type='local'),
    dcc.Store(id='selected-values2', storage_type='memory'),
    dcc.Store(id='selected-values_1', storage_type='memory'),
    dcc.Store(id='selected-values_2', storage_type='memory'),
    html.Div(id='common_DIV')
])


list_items_REV = [
    html.Li(f"{key}") for key, value in Manager_selections.items() if value
]


# Modal 1
modal_A = dbc.Modal(
    [
        # dbc.ModalHeader(dbc.ModalTitle("Rows Updated Successfully")),
        dbc.ModalHeader(dbc.ModalTitle(id="Modal_Title_Update")),
        dbc.ModalBody(id='ModalBody_REV_Updated',children=[]),
        dbc.ModalFooter(
            dbc.Button(
                "Back",
                id="Back_Button",
                className="ms-auto",
                n_clicks=0,
            )
        ),
    ],
    id="toggle_modal_1",
    keyboard=False,
    backdrop="static",
    is_open=False,
    centered=True,
    size="xl"
)


modal_val6 = False

modal6 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle("Alert..RECORDS already exist.....!!!"), close_button=True
                ),

                dbc.ModalBody(
                    # html.Ul(list_items_REV),
                    id='ModalBody_REV_2',
                    children=[]
                ),

                dbc.ModalFooter(dbc.Button("Update", id="Update_Button")),
            ],
            id="modal-dismiss6",
            keyboard=False,
            backdrop="static",
            is_open=modal_val6,
            centered=True,
            size="xl"
        ),
    ],
)




modal_val = False

modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle("Alert..RECORDS already exist.....!!!"), close_button=False
                ),

                dbc.ModalBody(
                    # html.Ul(list_items_REV),
                    id='ModalBody_REV',
                    children=[]
                ),

                # dbc.ModalBody(
                #     html.Ul(list_items_REV),
                #     id='ModalBody'
                # ),

                # dbc.ModalBody(
                #     'Vendor has a record already...'
                # ),

                dbc.ModalFooter(dbc.Button("Close", id="close-dismiss")),
            ],
            id="modal-dismiss",
            keyboard=False,
            backdrop="static",
            is_open=modal_val,
            centered=True,
            size="xl"
        ),
    ],
)

modal_val2 = False

modal2 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle("Alert..!!!"), close_button=False
                ),
                dbc.ModalBody(
                    'Please select any value...'
                ),
                dbc.ModalFooter(dbc.Button("Close", id="close-dismiss2")),
            ],
            id="modal-dismiss2",
            keyboard=False,
            backdrop="static",
            is_open=modal_val2,
            centered=True
        ),
    ],
)


modal_val3 = False

modal3 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle("Alert..!!!"), close_button=False
                ),
                dbc.ModalBody(
                    ' Please Select all 3 types of below information : '
                ),

                dbc.ModalBody(
                    html.Ul(
                        [
                            html.Li("Select atleast a Vendor detail"),
                            html.Li("Select atleat a Rebates value"),
                            html.Li("Select atleast Sales Slabs and Rebates"),
                        ]
                    )
                ),

                dbc.ModalFooter(dbc.Button("Close", id="close-dismiss3")),
            ],
            id="modal-dismiss3",
            keyboard=False,
            backdrop="static",
            is_open=modal_val3,
            centered=True
        ),
    ],
)


modal_val4 = False

modal4 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle("Alert..!!!"), close_button=False
                ),
                dbc.ModalBody(
                    ' PLEASE SELECT THE DATES CORRECTLY.............'
                ),

                dbc.ModalFooter(dbc.Button("Close", id="close-dismiss4")),
            ],
            id="modal-dismiss4",
            keyboard=False,
            backdrop="static",
            is_open=modal_val4,
            centered=True
        ),
    ],
)

list_items = [
    html.Li(f"Select at least {key}") for key, value in Manager_selections.items() if value
]

modal5 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("Your Selections are : ", style={'font-family': 'Algerian', 'fontSize': '40px', 'fontWeight': 'bold',
                                                                 'color': '#40396F', 'marginLeft': '270px'}),
                html.Hr(style={'marginTop': '0.05px',
                        'borderWidth': '3px', 'color': '#40396F'}),
                dbc.ModalBody(
                    html.Ul(list_items),
                    id='ModalBody'
                ),
                dbc.ModalFooter(dbc.Button("Close", id="close-dismiss5")),
            ],
            id="modal-dismiss5",
            size='xl',
            is_open=False,  # Replace modal_val5 with the actual condition
        ),
    ],
)


Home_Page_Layout = html.Div([


    html.H1(' REBATE   TERMS   FORM   DETAILS ', style={"background-color": "lightblue", 'color': 'Gray', 'textAlign': 'center', 'width': '60%', 'padding': '10px', 'margin': 'auto', 'margin-top': '20px',
                                                        'font-family': 'Algerian'}),
    modal,
    modal2,
    modal3,
    modal4,
    modal5,
    modal6,
   
    modal_A,

    html.Div([

        html.Div([

            dcc.Dropdown(
                id='Vendor Supplier_Name',
                options=Supplier_Name,
                value=[],
                multi=True,
                style={'width': '75%', 'padding': '10px',
                       'margin-left': '25px'},
                placeholder='Select Supplier Name'
            ),

            dcc.Dropdown(
                id='Vendor Supplier_Number',
                options=Supplier_Number,
                value=[],
                multi=True,
                style={'width': '75%', 'padding': '10px'},
                placeholder='Select Suplier Number'
            ),

            dcc.Dropdown(
                id='Vendor Vendor_Prefix',
                options=vendor_prefix,
                value=[],
                multi=True,
                style={'width': '75%', 'padding': '10px'},
                placeholder='Select Vendor Prefix'
            ),


        ], style={'display': 'flex', 'flex-direction': 'row', 'margin-top': '1px'}),


        html.Div([

            dcc.Dropdown(
                id='Vendor GLCLASS',
                options=GLCLASS,
                value=[],
                multi=True,
                style={'width': '75%', 'padding': '10px',
                       'margin-left': '25px'},
                placeholder='Select GLCLASS'
            ),

            dcc.Dropdown(
                id='Vendor Classification',
                options=Classification,
                value=[],
                multi=True,
                style={'width': '75%', 'padding': '10px'},
                placeholder='Select Classification'
            ),

            dcc.Dropdown(
                id='Vendor Model',
                options=Model,
                value=[],
                multi=True,
                style={'width': '75%', 'padding': '10px'},
                placeholder='Select Model'
            ),


        ], style={'display': 'flex', 'flex-direction': 'row', 'margin-top': '45px', 'margin-bottom': '5px'})

    ], style={"background-color": "lightblue", 'padding': '20px', 'margin-top': '30px', 'width': '70%', 'margin-left': '14%'}),



    html.Div([

        html.Div([

            dcc.Dropdown(
                id='Rebate Rebate_Teritory',
                options=Teritory,
                value=[],
                multi=True,
                style={'width': '75%', 'padding': '10px',
                       'margin-left': '25px'},
                placeholder='Select Teritory'
            ),

            dcc.Dropdown(
                id='Rebate Rebate_Period_From',
                options=Rebate_Period_From,
                value=[],
                multi=True,
                style={'width': '75%', 'padding': '10px'},
                placeholder='Select Rebate Period From'
            ),

            dcc.Dropdown(
                id='Rebate Rebate_Period_TO',
                options=Rebate_Period_TO,
                value=[],
                multi=True,
                style={'width': '75%', 'padding': '10px'},
                placeholder='Select Rebate Period TO'
            ),


        ], style={'display': 'flex', 'flex-direction': 'row', 'margin-top': '15px'}),


        html.Div([

            dcc.Dropdown(
                id='Rebate Rebate_Frequency',
                options=Rebate_Frequency,
                value=[],
                multi=True,
                style={'width': '75%', 'padding': '10px',
                       'margin-left': '25px'},
                placeholder='Select Rebate Frequency'
            ),

            dcc.Dropdown(
                id='Rebate Rebate_Currency',
                options=Rebate_Currency,
                value=[],
                multi=True,
                style={'width': '75%', 'padding': '10px'},
                placeholder='Select Rebate Currency'
            ),


            dcc.Dropdown(
                id='Rebate Rebate_Type',
                options=Rebate_Type,
                value=[],
                multi=True,
                style={'width': '75%', 'padding': '10px'},
                placeholder='Select Rebate Type'
            ),

        ], style={'display': 'flex', 'flex-direction': 'row', 'margin-top': '45px', 'margin-bottom': '5px'})

    ], style={"background-color": "#EBBABA", 'padding': '20px', 'margin-top': '0.7px', 'width': '70%', 'margin-left': '14%'}),


    # ***********************************************************************************************************************************************************************

    html.Div([


        html.Div([

            dcc.Dropdown(
                id='InputSalesAmount',
                options=Slabs,
                value=[],
                multi=True,
                style={'width': '90%', 'padding': '20px'},
                placeholder='Select Rebate Type'
            ),

            dcc.Dropdown(
                id='InputRebatesMargin',
                options=Rebates,
                value=[],
                multi=True,
                style={'width': '90%', 'padding': '20px'},
                placeholder='Select Rebate Type'
            )

        ], style={'display': 'flex', 'flex-direction': 'row', 'margin-top': '1px', 'margin-left': '5%'})


    ], style={"background-color": "#CACACA", 'padding': '1px', 'margin-top': '20px', 'width': '57%', 'margin-left': '20%'}),


    # ***********************************************************************************************************************************************************************


    dbc.Button("Update",  id="Update", n_clicks=0,  outline=True, color="secondary", className="me-1", style={'padding': '10px', 'width': '21%', 'margin-left': '26.5%', 'margin-top': '4%',
                                                                                                              "font-size": "30px", "font-weight": "bold", 'font-family': 'algerian'}),

    dbc.Button("Submit",  id="Submit", n_clicks=0,  outline=True, color="secondary", className="me-1", style={'padding': '10px', 'width': '21%', 'margin-left': '0%', 'margin-top': '4%',
                                                                                                              "font-size": "30px", "font-weight": "bold", 'font-family': 'algerian'}),

    dbc.Button("Logout", id="Logout1", href='/', n_clicks=0,  outline=True, color="secondary", className="me-1", style={'padding': '10px', 'width': '21%', 'margin-left': '0%', 'margin-top': '4%',
                                                                                                                        "font-size": "30px", "font-weight": "bold", 'font-family': 'algerian'})

])

Result_layout = html.Div([

    html.Div([
        html.H2('YOUR Current Selections are here: ',
                style={"background-color": "lightblue", 'color': 'Gray', 'textAlign': 'center', 'width': '60%',
                       'padding': '15px', 'margin': 'auto', 'margin-top': '20px',
                       'font-family': 'Algerian'})]),

    html.Div('TEST', id='selection_container',
             style={"background-color": "#E8E3E3", 'color': 'black', 'textAlign': 'center', 'width': '950px',
                    'margin-top': '40px', 'margin-left': '440px', 'padding': '40px',
                    'font-family': 'cambria'}),

    dbc.Button("Back", href='/HomePage', id="Back", n_clicks=0, outline=True, color="secondary", className="me-1",
               style={'padding': '10px', 'width': '21%', 'margin-left': '700px', 'margin-top': '5%',
                      "font-size": "30px", "font-weight": "bold", 'font-family': 'algerian'})

])

def generate_table(dataframe, exclude_first_column=False):
    return dash_table.DataTable(
        id='table',
        columns=[
            {"name": i, "id": i} for i in dataframe.columns
        ],
        page_size=50,
        data=dataframe.to_dict('records'),
        editable=True,  # Make cells editable
        row_selectable="multi",  # Allow selecting multiple rows
        selected_rows=[],  # Store selected rows
        style_table={
            'overflowX': 'auto',  # Horizontal scrolling
            'height':'700px',
            'maxHeight': '900px',  # Set a max height for vertical scrolling
        },
        style_cell={
            'textAlign': 'left',  # Align text to the left
            'whiteSpace': 'normal',  # Wrap text
            'height': 'auto',  # Adjust row height for wrapped text
            'minWidth': '150px',  # Minimum width for each column
            'maxWidth': '300px',  # Maximum width for each column
            'width': '100px',  # Default column width
        },
        style_header={
            'fontWeight': 'bold',  # Bold headers
            'height':'50px',
            'textAlign': 'center',
            'backgroundColor': '#f4f4f4',  # Add background color for headers
            'whiteSpace': 'normal',  # Wrap text in headers
        },
        fill_width=True,  # Disable automatic resizing of columns to table width
        fixed_rows={'headers': True}  # Keep headers fixed when scrolling
    )



columns = ['USER', 'Date', 'status', 'Supplier_Name', 'Supplier_Number', 'Vendor_Prefix', 'GLCLASS', 'Classification',
           'Model', 'Rebate_Teritory', 'Rebate_Type', 'Rebate_Frequency', 'Rebate_Period_From', 'Rebate_Period_TO',
           'Rebate_Currency', 'InputSalesAmount', 'InputRebatesMargin']


conn = sqlite3.connect('assets/Dash_Rebate_Database.db')
cursor = conn.cursor()

data_try = pd.read_sql('SELECT * FROM Vendor_Selections', conn)
conn.close()


data_try = data_try.iloc[::-1].reset_index(drop=True)
data_try['status'] = 'Pending'


Manager_Layout = dbc.Container([
    html.Div([
        modal5,
        dcc.Store(id='selected-values3', storage_type='local'),
        html.Div([
            html.H2('UnApproved Rebates Records: ',
                    style={"background-color": "#5B5C6C", 'color': 'white', 'textAlign': 'center', 'width': '60%',
                           'padding': '25px', 'margin': 'auto', 'margin-top': '20px',
                           'font-family': 'Algerian'})]),
        html.Br(),
        html.Br(),
        html.Br(),

        html.Div([
            dcc.Dropdown(
                id='Dimensions',
                options=columns,
                multi=False,
                placeholder='Select Dimensions',
                style={
                    'width': '375px',
                    'padding': '15px',
                    'marginLeft': '-230px',
                    'fontWeight': 'bold',
                    'fontFamily': 'calibri',
                    'fontSize': '18px',  # Increase font size for the selected value
                    'color': 'black',  # Text color
                    'backgroundColor': 'white'  # Dropdown background color
                }
            ),
           
            dcc.Download(id="download-table-data"),
           
           
            dcc.Dropdown(
                id='Dimensions_Values',
                options=[],
                multi=True,
                placeholder='Select a Dimension First...',
                style={
                    'width': '375px',
                    'padding': '15px',
                    'marginLeft': '-20px',
                    'marginTop': '-48px',
                    'fontWeight': 'bold',
                    'fontFamily': 'calibri',
                    'fontSize': '18px',  # Increase font size for the selected value
                    'color': 'black',  # Text color
                    'backgroundColor': 'white'  # Dropdown background color
                }
            ),
        ]),
       
       

        dbc.Button("Selections", id="Selections", n_clicks=0, outline=True, color="secondary", className="me-1",
                   style={'position': 'relative', 'padding': '18px', 'width': '200px', 'marginTop': '-120px',
                          "font-size": "20px", "font-weight": "bold", 'font-family': 'algerian',
                          'borderRadius': '120px', 'margin-left': '510px'}),
        dbc.Button("Select All", id='select_all_button', n_clicks=0, outline=True, color="secondary", className="me-1",
                   style={'position': 'relative', 'padding': '18px', 'width': '220px', 'marginTop': '-170px',
                          "font-size": "20px", "font-weight": "bold", 'font-family': 'algerian', 'z-index': '100',
                          'borderRadius': '120px', 'margin-left': '710px'}),
        dbc.Button("Approve", id="Approved", n_clicks=0, outline=True, color="secondary", className="me-1",
                   style={'position': 'relative', 'padding': '18px', 'width': '200px', 'marginTop': '-220px',
                          "font-size": "20px", "font-weight": "bold", 'font-family': 'algerian',
                          'borderRadius': '120px', 'margin-left': '931px'}),
        dbc.Button("Reject", id="Rejected", n_clicks=0, outline=True, color="secondary", className="me-1",
                   style={'position': 'relative', 'padding': '18px', 'width': '200px', 'marginTop': '-270px',
                          "font-size": "20px", "font-weight": "bold", 'font-family': 'algerian',
                          'borderRadius': '120px', 'margin-left': '1130px'}),
        dbc.Button("Export", id="export-button", n_clicks=0, outline=True, color="secondary", className="me-1",
                   style={'position': 'relative', 'padding': '18px', 'width': '220px', 'marginTop': '-320px',
                          "font-size": "20px", "font-weight": "bold", 'font-family': 'algerian', 'z-index': '100',
                          'borderRadius': '120px', 'margin-left': '1330px'}),
        dbc.Button("Submit23", id="Submit23", n_clicks=0, outline=True, color="secondary", className="me-1",
                   style={'position': 'relative', 'padding': '18px', 'width': '220px', 'marginTop': '-370px',
                          "font-size": "20px", "font-weight": "bold", 'font-family': 'algerian', 'z-index': '100',
                          'borderRadius': '120px', 'margin-left': '1550px'}),
        dbc.Button("Back", id="Back2", n_clicks=0, outline=True, color="secondary", className="me-1",
                   style={'position': 'relative', 'padding': '18px', 'width': '200px', 'marginTop': '-320px',
                          "font-size": "20px", "font-weight": "bold", 'font-family': 'algerian',
                          'borderRadius': '120px', 'margin-left': '1550px'}),
        dbc.Button("LOGOUT", id='Logout2', href='/', n_clicks=0, outline=True, color="secondary", className="me-1",
                   style={'position': 'relative', 'padding': '18px', 'width': '220px', 'marginTop': '-600px',
                          "font-size": "20px", "font-weight": "bold", 'font-family': 'algerian', 'z-index': '100',
                          'borderRadius': '120px', 'margin-left': '1550px'}),

        dbc.Row([
            dbc.Col(html.Div(id='table-container', children=generate_table(data_try,False),
                              style=table_container_style), width={"size": 12})
        ])
       
    ])
])
# ============================================= NORMAL FUNCTIONS TO OPTIMIZE THE CODE ====================================================================


def flatten_list(nested_list):
    return [item for sublist in nested_list for item in (flatten_list(sublist) if isinstance(sublist, list) else [sublist])]


def UpdateDataset():
    global filtered_data, Vendor_selection, Vendor_Var

    for i in Vendor_Seq_List:
        if Vendor_selection[i] is not None and len(Vendor_selection[i]) > 0:
   
            if "SELECT_ALL" in Vendor_selection[i]:
                Vendor_selection[i] = ['SELECT_ALL']
                Vendor_Var = Vendor_Seq_List.index(i)
                continue
            else:
               
                filtered_data = filtered_data[filtered_data[i.split()[1]].isin(Vendor_selection[i])]
                Vendor_Var = Vendor_Seq_List.index(i)

    filtered_data = filtered_data.reset_index(drop=True)
    filtered_data.loc[len(filtered_data)] = "SELECT_ALL"


def UpdateVariable():

    global filtered_data, Supplier_Name_1, Supplier_Number_1, Vendor_Prefix_1, GLCLASS_1, Classification_1, Model_1

    Supplier_Name_1 = sorted(list(set(filtered_data['Supplier_Name'])), key=lambda x: (isinstance(x, str), x), reverse=True)
    Supplier_Number_1 = sorted(list(set(filtered_data['Supplier_Number'])), key=lambda x: (isinstance(x, str), x), reverse=True)
    Vendor_Prefix_1 = sorted(list(set(filtered_data['Vendor_Prefix'])), key=lambda x: (isinstance(x, str), x), reverse=True)
    GLCLASS_1 = sorted(list(set(filtered_data['GLCLASS'])), key=lambda x: (isinstance(x, str), x), reverse=True)
    Classification_1 = sorted(list(set(filtered_data['Classification'])), key=lambda x: (isinstance(x, str), x), reverse=True)
    Model_1 = sorted(list(set(filtered_data['Model'])), key=lambda x: (isinstance(x, str), x), reverse=True)
   
   
   
   
@app.callback(
    Output('table', 'selected_rows'),
    Input('select_all_button', 'n_clicks'),
    State('table', 'data'),
    State('table', 'selected_rows')
)
def toggle_select_all(n_clicks, table_data, selected_rows):
    if n_clicks % 2 == 1:
        # If n_clicks is odd, select all rows
        return list(range(len(table_data)))
    else:
        # If n_clicks is even, deselect all rows
        return []
 
   
 
@app.callback(
    Output("download-table-data", "data"),
    Input("export-button", "n_clicks"),
    prevent_initial_call=True
)
def export_table(n_clicks):
    global data_try_temp_3
    return dcc.send_data_frame(data_try_temp_3.to_csv, "table_data.csv")
 
   
   
   
   
# ============================================= NORMAL FUNCTIONS TO OPTIMIZE THE CODE ====================================================================

# ========================================================================================================================================================
@app.callback(
    [Output("modal-dismiss5",  "is_open"),
     Output("ModalBody",  "children")],
    [Input("Selections",  "n_clicks"),
     Input("close-dismiss5",  "n_clicks")], prevent_initial_call=True
)
def toggle_modal(n_clicks, n_clicks2):
    print('Callback 22222222\n')
    global Manager_selections, list_items, list_items1, Final_List
    Final_List = []

    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    for key, value in Manager_selections.items():
        if value:
            list_items = [html.Li(f"{key}", style={'font-family': 'Algerian', 'fontSize': '20px',
                                                   'fontWeight': 'bold', 'color': '#40396F', 'marginTop': '35px'})]
            list_items1 = [html.Li(f"{value}", style={'font-family': 'Tahoma', 'fontSize': '17px',
                                                      'fontWeight': 'bold', 'color': '#908585', 'marginTop': '35px'})]

            for i, ii in zip(list_items, list_items1):
                Final_List.append(i)
                Final_List.append(ii)

    if triggered_id == 'Selections':
        return [True, Final_List]

    elif triggered_id == 'close-dismiss5':
        return [False, Final_List]

    else:
        return [False, Final_List]


@app.callback(
    Output('Dimensions_Values', 'value'),
    Output('Back2', 'style'),
    Output('Selections', 'style'),
    Output('Approved', 'style'),
    Output('Rejected', 'style'),
    Output('Submit23', 'style'),
    Output('select_all_button', 'style'),
    Output('export-button', 'style'),
    Output('Logout2', 'style'),
    Output('selected-values3', 'data'),
    Output('Dimensions_Values', 'options'),
    Input('Dimensions', 'value'),
    Input('Approved', 'n_clicks'),
    Input('Rejected', 'n_clicks'),
    Input('Submit23', 'n_clicks'),
    Input('Back2', 'n_clicks'),
    State('table','selected_rows')          
)
def callback1(Dimension, Approved, Rejected, Submit, Back2, selected_rows):
    print('Callback 33333333')
   
    global data_try, data_try_temp,  selections_checklist
    global status_update , var1, var2, var3
    global table_container_style
   
    col_value = temp_values = var1 = var2 = var3 = []

    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if Dimension and Dimension in Manager_selections:
        temp_values = Manager_selections[Dimension] if Manager_selections[Dimension] else temp_values

    back = {'display': 'None'}
    selections = approved = rejected = submit = select_all = export = Logout = dash.no_update
   
    table_container_style['margin-top'] = '-100px'


    if 'Submit23' in triggered_id:
       
        table_container_style['margin-top'] = '25px'

        back = {'position': 'relative', 'padding': '18px', 'width': '220px', 'marginTop': '-130px',
               "font-size": "20px", "font-weight": "bold", 'font-family': 'algerian', 'z-index': '100',
               'borderRadius': '120px', 'margin-left': '1550px'}
       
        Logout={'position': 'relative', 'padding': '18px', 'width': '220px', 'marginTop': '-450px',
               "font-size": "20px", "font-weight": "bold", 'font-family': 'algerian', 'z-index': '100',
               'borderRadius': '120px', 'margin-left': '1550px'}

        selections = approved = rejected = submit = select_all = export = {'display': 'None'}
        First_Col = True  
       
        data_to_update = []

        if status_update['Approved'] is not None:
            print('check 1...........................................')
            data_to_update.append(status_update['Approved'])
            var1 = data_try[data_try['status']=='Approved']['index_1'].to_list()
           
        if status_update['Rejected'] is not None:  
            print('check 2...........................................')
            data_to_update.append(status_update['Rejected'])
            var2 = data_try[data_try['status']=='Rejected']['index_1'].to_list()
           

        var3 = flatten_list([var1,var2])
        print('var3 values are : ' , var3)
        my_placeholder_1 = ', '.join(['?'] * len(var1))
        my_placeholder_2 = ', '.join(['?'] * len(var2))
        my_placeholder_3 = ', '.join(['?'] * len(var3))
       
       
        if (var1 or var2) and var3:
            print('its working till here')
           
            query = f'''
                UPDATE Vendor_Selections
                SET status = CASE
                    WHEN index_1 IN ({my_placeholder_1}) THEN 'Approved'
                    WHEN index_1 IN ({my_placeholder_2}) THEN 'Rejected'
                END
                WHERE index_1 IN ({my_placeholder_3});
                '''  
               
            conn = sqlite3.connect('assets/Dash_Rebate_Database.db')
            cursor = conn.cursor()
           
            all_values = tuple(var1 + var2 + var3)
           
            conn.execute(query,all_values)
           
            conn.commit()
            conn.close()
           
            print('query values are ::::::::::' , query)


    elif 'Back2' in triggered_id:

        table_container_style['margin-top'] = '-100px'

        back = {'display': 'None'}

       
        selections = {'position': 'relative', 'padding': '18px', 'width': '200px', 'marginTop': '-120px',
                          "font-size": "20px", "font-weight": "bold", 'font-family': 'algerian',
                          'borderRadius': '120px', 'margin-left': '510px'}
        select_all = {'position': 'relative', 'padding': '18px', 'width': '220px', 'marginTop': '-170px',
                          "font-size": "20px", "font-weight": "bold", 'font-family': 'algerian', 'z-index': '100',
                          'borderRadius': '120px', 'margin-left': '710px'}
        approved = {'position': 'relative', 'padding': '18px', 'width': '200px', 'marginTop': '-220px',
                          "font-size": "20px", "font-weight": "bold", 'font-family': 'algerian',
                          'borderRadius': '120px', 'margin-left': '931px'}
        rejected = {'position': 'relative', 'padding': '18px', 'width': '200px', 'marginTop': '-270px',
                          "font-size": "20px", "font-weight": "bold", 'font-family': 'algerian',
                          'borderRadius': '120px', 'margin-left': '1130px'}
        export = {'position': 'relative', 'padding': '18px', 'width': '220px', 'marginTop': '-320px',
                          "font-size": "20px", "font-weight": "bold", 'font-family': 'algerian', 'z-index': '100',
                          'borderRadius': '120px', 'margin-left': '1330px'}
        submit = {'position': 'relative', 'padding': '18px', 'width': '220px', 'marginTop': '-370px',
                          "font-size": "20px", "font-weight": "bold", 'font-family': 'algerian', 'z-index': '100',
                          'borderRadius': '120px', 'margin-left': '1550px'}
        Logout = {'position': 'relative', 'padding': '18px', 'width': '220px', 'marginTop': '-600px',
                          "font-size": "20px", "font-weight": "bold", 'font-family': 'algerian', 'z-index': '100',
                          'borderRadius': '120px', 'margin-left': '1550px'}
       
       
 
    if 'Approved' in triggered_id or 'Rejected' in triggered_id :

        data_try_temp = data_try.copy()
       
        for key, values in Manager_selections.items():
            data_try_temp = data_try_temp[data_try_temp[key].isin(values)] if values else data_try_temp
       
        array1 = np.array(data_try_temp.index)
        rows_to_Update = array1[selected_rows]
       
        data_try.loc[rows_to_Update , 'status'] = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
       
        array1 = np.array(data_try_temp['index_1'])
        rows_to_Update = array1[selected_rows]  
       
        status_update[triggered_id] = rows_to_Update
       
        print('status_update values are :::::   CHEKCING BEFORE' , status_update)

         
    if Dimension:
        if Dimension not in selections_checklist:
            # print('condition 111111111111111111111111')
            data_try_temp = data_try.copy()

            for key, values in Manager_selections.items():
                data_try_temp = data_try_temp[data_try_temp[key].isin(values)] if values else data_try_temp

            col_value = data_try_temp[Dimension].unique().tolist()
            col_value = sorted(col_value, key=lambda x: x is None)
            selections_checklist.append(Dimension)

        else:
            # print('condition 2222222222222222222222222222')
            data_try_temp = data_try.copy()

            for key, values in Manager_selections.items():

                if Dimension == selections_checklist[0]:
                    # print('condition 33333333333333333333333')
                    selections_checklist = [Dimension]

                    for key in list(Manager_selections.keys())[1:]:
                        Manager_selections[key] = None

                    continue

                elif key != Dimension:
                    data_try_temp = data_try_temp[data_try_temp[key].isin(
                        values)] if values else data_try_temp

                else:
                    selections_checklist = selections_checklist[:selections_checklist.index(
                        key)]

                    for key in list(Manager_selections.keys())[len(selections_checklist):]:
                        Manager_selections[key] = None
                    break

           
            print('\n')
            print('data_try_temp values are : ' , data_try_temp)
       
            col_value = data_try_temp[Dimension].unique().tolist()
            col_value = sorted(col_value, key=lambda x: x is None)

    # print('data_try Supplier name :\n' , list(data_try['Supplier Name'].unique()))
   
    # print('data_try_temp values after update: ', data_try)
   
    return temp_values, back, selections, approved, rejected, submit, select_all, export , Logout, col_value, col_value





@app.callback(
    Output('Dimensions_Values', 'options', allow_duplicate=True),
    Output('table-container', 'style', allow_duplicate=True),
    Output('table-container', 'children', allow_duplicate=True),
    Input('Dimensions_Values', 'value'),
    Input('selected-values3', 'data'),
    State('Dimensions', 'value'),
    State('Dimensions_Values', 'value'), prevent_initial_call=True
)
def callback2(Dimension_values, storage_values, Dimensions, Dimensions_Values):
    print('Callback 444444444')

    global data_try_temp_2, data_try_temp_3, data_try, Manager_selections, columns, table_container_style, status_val, selections_checklist
    global table_container_style
   
   
   
    data_try_temp_2 = data_try.copy()
    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    # data_try_temp_2.reset_index(inplace=True) if 'index' not in list(data_try_temp_2.columns) else data_try_temp_2

    for key, values in Manager_selections.items():

        if key == Dimensions and not Dimensions_Values:

            if key == selections_checklist[0]:
                selections_checklist = [Dimensions]

                for key in Manager_selections:
                    Manager_selections[key] = None
                break

            else:
                for key, values in Manager_selections.items():
                    Manager_selections[key] = None if key not in selections_checklist else Manager_selections[key]
                break
        else:
            data_try_temp_2 = data_try_temp_2[data_try_temp_2[key].isin(
                values)] if values else data_try_temp_2

    if Dimensions and Dimensions_Values and triggered_id != 'selected-values':
        Manager_selections[Dimensions] = Dimensions_Values
        data_try_temp_2 = data_try.copy()
        data_try_temp_2.reset_index(inplace=True)

        for key, values in Manager_selections.items():
            data_try_temp_2 = data_try_temp_2[data_try_temp_2[key].isin(
                values)] if values else data_try_temp_2

            if key in Dimensions:
                break

    Manager_selections = {key: value for key,
                          value in Manager_selections.items() if value is not None}

    # print('data_try Supplier name :\n' , list(data_try['Supplier Name'].unique()))
    # columns_to_keep = ['status','USER', 'Date', 'Supplier_Name', 'Supplier_Number', 'Vendor_Prefix', 'GLCLASS', 'Classification', 'Model',
    #                    'Rebate_Teritory', 'Rebate_Type', 'Rebate_Frequency', 'Rebate_Period_From', 'Rebate_Period_TO', 'Rebate_Currency',
    #                    'InputSalesAmount', 'InputRebatesMargin']
   
    data_try_temp_3         = data_try_temp_2.copy()
    data_try_temp_3         = data_try_temp_2[columns]
    data_try_temp_3.columns = columns
   
    # data_try_temp_3.columns = ['Status','User', 'Date', 'Supplier Name', 'Supplier Number', 'Vendor Prefix', 'GLCLASS', 'Classification', 'Model',
    #                    'Rebate Teritory', 'Rebate Type', 'Rebate Frequency', 'Rebate Period From', 'Rebate Period TO', 'Rebate Currency',
    #                    'Slabs', 'Rebate Margin']

    return storage_values, table_container_style, generate_table(data_try_temp_3, False)

# =========================================================================================================================================

# ============================================= USER LOGIN  ====================================================================

@app.callback([
    Output('Login_Output',  'children'),
    Output('url2',  'pathname',   allow_duplicate=True),
    Output('url3',  'pathname',   allow_duplicate=True)],
    Input('Submit_Login',  'n_clicks'),
    State('Username',  'value'),
    State('Password',  'value'), prevent_initial_call=True
)
def User_Login(n_clicks_submit, user_id, password):
    print('Callback 555555555')
    global VALID_USERNAME

    if n_clicks_submit and n_clicks_submit > 0:

        if user_id == 'user' and password == 'user':
            VALID_USERNAME = 'user'
            return dash.no_update, '/HomePage', dash.no_update

        elif user_id == 'admin' and password == 'admin':
            VALID_USERNAME = 'admin'
            return dash.no_update, dash.no_update, '/Approval'

        else:
            return html.Div([html.P('WRONG CREDENTIALS')]), dash.no_update, dash.no_update

    else:
        return dash.no_update, dash.no_update, dash.no_update   # Added return statement here

# ============================================= USER LOGIN  ====================================================================


@app.callback(
    Output('common_DIV', 'children'),
    [Input('url', 'pathname'),
     Input('url2', 'pathname'),
     Input('url3', 'pathname')]
)
def display_page(pathname, pathname2, pathname3):
    print('Callback 666666666666')
    global modal_val, navigate, modal_val2, filtered_data_try, Supplier_Name_1, Supplier_Name, Supplier_Number_1, Supplier_Number
    global Vendor_Prefix_1, vendor_prefix, GLCLASS_1, GLCLASS, Classification_1, Classification, Model_1, Model
    global data_try, data2, Teritory, Rebate_Currency, Teritory_Currency
    global status_update, Manager_selections

    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if pathname3 and len(pathname3) > 3:
        pathname = pathname3

    elif pathname2 and len(pathname2) > 3:
        pathname = pathname2

    if pathname == '/':
        if triggered_id != 'url':
            if VALID_USERNAME is not None and VALID_USERNAME == 'user':
                return Home_Page_Layout
            elif VALID_USERNAME is not None and VALID_USERNAME == 'admin':
                return Manager_Layout
            else:
                return Login_Layout
        else:
            return Login_Layout

    elif pathname == '/HomePage' and VALID_USERNAME == 'user':

        modal_val = False
        navigate = '/HomePage'
        modal_val2 = False

        filtered_data = data.copy()
        Vendor_Seq_List = []

        for i in Vendor_selection.keys():
            Vendor_selection[i] = None

        Supplier_Name_1 = Supplier_Name = sorted(list(
            set(data['Supplier_Name'])), key=lambda x: (isinstance(x, str), x), reverse=True)
        Supplier_Number_1 = Supplier_Number = sorted(list(set(
            data['Supplier_Number'])), key=lambda x: (isinstance(x, str), x), reverse=True)
        Vendor_Prefix_1 = vendor_prefix = sorted(list(
            set(data['Vendor_Prefix'])), key=lambda x: (isinstance(x, str), x), reverse=True)
        GLCLASS_1 = GLCLASS = sorted(list(set(data['GLCLASS'])), key=lambda x: (
            isinstance(x, str), x), reverse=True)
        Classification_1 = Classification = sorted(list(
            set(data['Classification'])), key=lambda x: (isinstance(x, str), x), reverse=True)
        Model_1 = Model = sorted(list(set(data['Model'])), key=lambda x: (
            isinstance(x, str), x), reverse=True)

        Teritory = sorted(list(set(data2['Rebate_Teritory'])), key=lambda x: (
            isinstance(x, str), x), reverse=True)
        Rebate_Currency = sorted(list(set(data2['Rebate_Currency'])), key=lambda x: (
            isinstance(x, str), x), reverse=True)

        return Home_Page_Layout

    elif pathname == '/result' and VALID_USERNAME == 'user':
        return Result_layout

    elif pathname == '/Approval' and VALID_USERNAME == 'admin':
        # print('working till here........')
        conn = sqlite3.connect('assets/Dash_Rebate_Database.db')

        cursor = conn.cursor()

        data_try = pd.read_sql('SELECT * FROM Vendor_Selections', conn)
       
       
        if data_try is None or data_try.empty:
            print("data_try is empty or None")
        else:
            if data_try.index[0] != data_try.index.max():
                data_try = data_try.iloc[::-1].reset_index(drop=True)
                # data_try.sort_values(by='Date', ascending=False, inplace=True)

        conn.close()

        d = data_try.copy()
        selections_checklist = []
        Manager_selections = {}
        data_try_temp_2 = data_try_temp = data_try.copy()
       
        status_update  = {'Approved':None,'Rejected':None}

        return Manager_Layout

    else:
        return '404 Page Not Found'


Vendor_selection_rev = dict()

# # ===============================================================================================================


@app.callback(
    Output('selected-values_1', 'data'),
    [Input('Update', 'n_clicks'),
     Input('Submit', 'n_clicks')],
    prevent_initial_call=True
)
def Storing_Selections(n_clicks, n_clicks2):
    print('Callback 77777777777')
   
    global Vendor_selection, navigate, modal_val, modal_val2, modal_val3, modal_val4, modal_val6
    global Vendor_selection_rev
   
    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
   
    # Initialize default values
    Vendor_selection_rev = dash.no_update
    modal_val = False
    modal_val2 = False
    modal_val3 = False
    modal_val4 = False
    modal_val6 = False
    navigate = dash.no_update
   
    # Check if the callback is triggered correctly
    if (n_clicks > 0 or n_clicks2 > 0) and Vendor_selection and any(Vendor_selection.values()):
        checklist = str([key for key, value in Vendor_selection.items() if value])

        # Validate checklist conditions
        if 'Vendor' in checklist and 'Rebate' in checklist and 'InputSalesAmount' in checklist and 'InputRebatesMargin' in checklist:
           
            temp1 = datetime.strptime(Vendor_selection['Rebate Rebate_Period_From'][0], '%d-%b-%Y') if 'Rebate_Period_From' in checklist else ''
            temp2 = datetime.strptime(Vendor_selection['Rebate Rebate_Period_TO'][0], '%d-%b-%Y')   if 'Rebate_Period_TO' in checklist else ''
           
            temp3 =  Vendor_selection['Rebate Rebate_Period_From'] if 'Rebate_Period_From' in checklist else ''
            temp4 =  Vendor_selection['Rebate Rebate_Period_TO']   if 'Rebate_Period_TO' in checklist else ''

            # Validate period range
            if temp1 and temp2 and temp1 < temp2 and len(temp3) == 1 and len(temp4) == 1:
                # print("Vendor_selection values are:", Vendor_selection)

                # Process Vendor_selection
                # Vendor_selection_rev = {(key.split()[1] if 'Input' not in key else key): [value] for key, value in Vendor_selection.items() if str(value) != 'None'}
                Vendor_selection_rev = {(key.split()[1] if 'Input' not in key else key): [value] for key, value in Vendor_selection.items() if str(value) != 'None'}

                print("\nVendor_selection_rev values are:\n", Vendor_selection_rev)
                return [True,triggered_id]
            else:
                print("Invalid date range or missing data.")
                modal_val4 = True
                return [False,triggered_id]
        else:
            print("Checklist conditions not met.")
            modal_val3 = True
            return [False,triggered_id]
    elif n_clicks > 0 or n_clicks2 > 0:
        print("Invalid Vendor_selection data.")
        modal_val2 = True
        return [False,triggered_id]

    return [False,triggered_id]



@app.callback(
    Output('selected-values_2', 'data'),
    Input('selected-values_1', 'data') , prevent_initial_call=True)    
def func_2(pass_code):
   
    print('Callback 7.......AAAAAAA')
    if pass_code[0]:
       
        global filtered_data, Vendor_selection, modal_val, navigate, modal_val2, modal_val3, modal_val4, modal_val6, df_from_sql
        global VALID_USERNAME, Vendor_selection_rev, common_rows_rev
        global df , df_from_sql, temp_df
       
        df = filtered_data.copy()
   
        df = df[df['Supplier_Name'] != 'SELECT_ALL']
   
        df = df.drop(columns='KEY') if 'KEY' in list(df.columns) else df
   
        for i in df.columns:
            df[i] = df[i].apply(lambda x: str(x) if x is not None else '')
   
        df['USER'] = VALID_USERNAME
        df['status'] = 'Pending'
        df['Date'] = datetime.now().date()
   
        for key, value in Vendor_selection_rev.items():
            if value and str(value) != 'None':
                if 'Vendor' not in key and 'SELECT_ALL' not in value[0]:
                    if len(flatten_list(value)) > 1:
                        temp_df = pd.DataFrame({key.split()[-1]: flatten_list(value)})
                        df = pd.merge(df, temp_df, how='cross')
                    else:
                        df[key.split()[-1]] = flatten_list(Vendor_selection_rev[key])[0]
       
       
        # df['KEY'] = df.apply(lambda x: ''.join(x.values.astype(str)) if x is not None else '', axis=1)
        # List of columns to ignore
        ignore_columns = ['USER', 'Select', 'index_1']
       
        # Exclude the ignored columns from the concatenation
        df['KEY'] = df.apply(lambda x: ''.join(x[~x.index.isin(ignore_columns)].astype(str)) if x is not None else '', axis=1)

        # print('KEy values is \n', df['KEY'])
       
        query = ''
   
        for key, value in Vendor_selection_rev.items():
            # print('values is ::::::::::' , value)
            if value[0] and str(value[0]) != 'None' and 'SELECT_ALL' not in value[0]:
                print(1)
                key = key.split()[-1]
                value = str(flatten_list(value))[1:-1]
                query = query + f"{key} in ({value}) AND "
   
        query = 'Select * from Vendor_Selections WHERE ' + query[:-4]
       
       
        query = query.replace("\n", "")
   
        # print('query values are : ' , query)
       
        # conn = sqlite3.connect(#'C:/Users/ASUS/Documents/Rebate System Project/Dash_Rebate_Database.db')
        conn = sqlite3.connect('assets/Dash_Rebate_Database.db')
   
        cursor = conn.cursor()
   
        table_exists = cursor.fetchone()
   
        df_from_sql = pd.read_sql(query, conn)
   
        # Convert the 'KEY' column in both DataFrames to string type before merging
        df['KEY'] = df['KEY'].astype(str)
        df_from_sql['KEY'] = df_from_sql['KEY'].astype(str)
           
        query = "SELECT count(*) FROM Vendor_Selections"
        last_index = pd.read_sql_query(query, conn).iloc[0, 0]
       
        df['index_1'] = range(last_index , last_index + len(df))
       
        # print('df checking df values is :::::::::::' , df)
       

        return [True,pass_code[-1]]

    return [False,pass_code[-1]]


@app.callback(
    Output('selected-values', 'data'),
    Output('ModalBody_REV_2', 'children'),
    Output('ModalBody_REV', 'children'),
    Output('modal-dismiss', 'is_open', allow_duplicate=True),
    Output('modal-dismiss2', 'is_open', allow_duplicate=True),
    Output('modal-dismiss3', 'is_open', allow_duplicate=True),
    Output('modal-dismiss4', 'is_open', allow_duplicate=True),
    Output('modal-dismiss6', 'is_open', allow_duplicate=True),
    Output('url', 'pathname'),
    Input('selected-values_2', 'data'),
    prevent_initial_call=True
)
def func_3(pass_code_2):
    print('Callback 7.......BBBBBBBBBBB')
    if pass_code_2[0]:

        global filtered_data, Vendor_selection, modal_val, navigate, modal_val2, modal_val3, modal_val4, modal_val6
        global df, df_from_sql, common_rows_rev, common_rows_rev_2, columns, columns_seq
       
        common_rows_rev = None
        common_rows_rev_2 = None
       
        print('\n\n checkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk \n')
        print(df)
        print('\n')
        print(df_from_sql)
       
        triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
   
        conn = sqlite3.connect('assets/Dash_Rebate_Database.db')

        if not df_from_sql.empty:
            table = dash_table.DataTable(
                data=df_from_sql.to_dict("records"),
                columns=[{"name": col, "id": col, 'editable':True if col != 'status' else False} for col in df_from_sql.columns if col not in \
                                                                                                                     ['Select', 'KEY']],
                
                editable=True,
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left", "padding": "10px"},
                style_header={"backgroundColor": "lightgrey", "fontWeight": "bold"},
                style_data={"backgroundColor": "white"},
            )
            columns_seq = columns
            columns_seq.append('index_1') if 'index_1' not in columns_seq else columns_seq
            table.columns = [{"name": col, "id": col, 'editable':True if col != 'status' else False} for col in columns_seq]
               
            common_rows_rev_2  = df_from_sql.copy()
            # common_rows_rev_2 = common_rows_rev_2[columns]
               
           
            if pass_code_2[-1] == 'Submit':
                common_rows = pd.merge(df, df_from_sql, on=['KEY'])
                common_rows = common_rows.drop(columns=['KEY'])
               
                print(' common_rows.empty values are : ' ,  common_rows.empty)
       
                if not common_rows.empty and common_rows is not None:
                    print('\nthis condition is running ............................\n')
                    # Create DataTable for common rows
                   
                    common_rows_rev = table
                    # common_rows_rev = pd.DataFrame(table.data)[columns]
                    modal_val = True
                    navigate = dash.no_update
                   
                else:
                    print('ye chal rahi hai .................................................................')
                    df.to_sql('Vendor_Selections', conn, index=False, if_exists='append')
                    modal_val = False
                    navigate = '/result'
                    print('yaha tak chal gai hai.............................................................')
       
            elif pass_code_2[-1] == 'Update':  
                common_rows_rev = table
                # common_rows_rev = pd.DataFrame(table.data)[columns]
                modal_val6 = True
                navigate = dash.no_update
        else:
            print()
            print('ye chal rahi hai .................................................................')
           
            df.to_sql('Vendor_Selections', conn, index=False, if_exists='append')
            modal_val = False
            navigate = '/result'
           
            print('yaha tak chal gai hai.............................................................')
           
        conn.close()

    else:
        common_rows_rev = None
        common_rows_rev_2 = None
       
    return Vendor_selection, common_rows_rev, common_rows_rev, modal_val, modal_val2, modal_val3, modal_val4, modal_val6, navigate
# ======================================================================================================================================


# Callback to toggle Modal 1
@app.callback(
    Output('Modal_Title_Update','children'),
    Output('modal-dismiss6','is_open'),
    Output('toggle_modal_1','is_open'),
    Output('ModalBody_REV_Updated','children'),
    Input("Update_Button", "n_clicks"),
    State('ModalBody_REV_2', 'children'), prevent_initial_call=True
)
def Update_Button(n_clicks, updated_table):
   
    global df, common_rows_rev_2, combined, columns, columns_seq
   
    updated_table = updated_table["props"]["data"]
    updated_table = pd.DataFrame(updated_table)

    common_rows_rev_2 = common_rows_rev_2[columns_seq]
    updated_table = updated_table[columns_seq]
   
    common_data = pd.merge(common_rows_rev_2, updated_table, how='inner')
    updated_table = pd.concat([updated_table, common_data]).drop_duplicates(keep=False)
   
    updated_table = updated_table[columns]

   
    if n_clicks and not updated_table.empty:  
       
        indicies_to_Update = updated_table['index_1'].tolist()
       
        indicies_to_Update = np.array(indicies_to_Update, dtype=int)
        result = np.array(indicies_to_Update) - 1
        indicies_to_Update = result.tolist()
        indicies_to_Update = [str(val) if isinstance(val, tuple) else val for val in indicies_to_Update]
       
        combined_data_table = dash_table.DataTable(
        data=updated_table.to_dict('records'),
        columns=[{"name": col, "id": col} for col in updated_table.columns],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
        )
       
        conn = sqlite3.connect('assets/Dash_Rebate_Database.db')
        cursor = conn.cursor()
       
        # SQL_data_query = 'SELECT index_1 FROM Vendor_Selections WHERE index_1 = ?'
        # SQL_data = pd.read_sql(SQL_data_query, conn,  params=(indecies_to_Update,))
       
        # sql_query = f"SELECT index_1 FROM Vendor_Selections WHERE index_1 IN ({','.join(['?'] * len(indecies_to_Update))})"

        # # Execute query with the list as parameters
        # SQL_data = pd.read_sql_query(sql_query, conn, params=tuple(indecies_to_Update))
        print('df.columns values are ::::::::' , df.columns)
       
        columns_to_update = [col for col in df.columns if col not in ['status', 'Date', 'KEY']]
       
        print('columns_to_update valuesa are :::::: ' , columns_to_update)
   
        # Dynamically construct the SQL query
        set_clause = ", ".join([f"{col} = ?" for col in columns_to_update])
        sql_query = f"""UPDATE Vendor_Selections
        SET {set_clause}
        WHERE index_1 = ?
        """
        print('\n sql_query values are  \n', sql_query)
        # Iterate through DataFrame rows
        for _, row in updated_table.iterrows():
            print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
            print('\n _ values is :::::::: \n', _ )
            print('type(row) values are :' , type(row))
           
            update_values = [row[col] for col in columns_to_update]
            update_values.append(row['index_1'])
            print('\n update_values values are ::\n', update_values)
           
            # key_value = row['index_1']
            # key_value = index
   
            # Execute the SQL query with the parameters
            cursor.execute(sql_query, update_values)
            update_values = []
            # cursor.execute(sql_query, (*update_values, key_value))
       
        # Commit changes and close the connection
        conn.commit()
        cursor.close()
       
        # print('\n SQL_data values are :::::::::::::\n' , SQL_data)
       
        return  'Rows Updated Successfully' , False, True , combined_data_table
   
    return 'NO Row Updated ' , False, True, html.P(
        "No updates available. The table has no new data to display.",
        style={"color": "red", "textAlign": "center", "fontSize": "16px", "fontWeight":"bold"}
    )


# Callback to toggle Modal 1
@app.callback(
    Output('modal-dismiss6','is_open', allow_duplicate=True),
    Output('toggle_modal_1','is_open', allow_duplicate=True),
    Input("Back_Button", "n_clicks") , prevent_initial_call=True
)
def Update_Button(n_clicks):
    if n_clicks:
        return True, False
    return False, True



@app.callback(
    [Output("modal-dismiss",  "is_open"),
     Output("modal-dismiss2",  "is_open"),
     Output("modal-dismiss3",  "is_open"),
     Output("modal-dismiss4",  "is_open")],
    [Input("close-dismiss",  "n_clicks"),
     Input("close-dismiss2",  "n_clicks"),
     Input("close-dismiss3",  "n_clicks"),
     Input("close-dismiss4",  "n_clicks")]
)
def toggle_modal(n_clicks, n_clicks2, n_clicks3, n_clicks4):
    print('Callback 888888888888888')
    navigate = '/HomePage'
    modal_val = False
    modal_val2 = False
    modal_val3 = False
    modal_val4 = False

    if n_clicks or n_clicks2 or n_clicks3 or n_clicks4:
        return modal_val, modal_val2, modal_val3, modal_val4

    return dash.no_update, dash.no_update, dash.no_update, dash.no_update


# ===============================================================================================================

@app.callback(
    Output('selection_container', 'children'),
    [Input('selected-values', 'data')]
)
def Showing_Selections(data):
   
    global Vendor_selection

    Vendor_selection = data

    selected_values = {key: value for key, value in Vendor_selection.items() if value is not None}

    if any(selected_values.values()):

        divs = []

        for key in selected_values.keys():
            divs.append(

                html.Div([

                    html.Div([
                        html.P(str(key)),
                    ], style={'display': 'inline-block', 'textAlign': 'center', 'fontWeight': 'bold',
                              'color': '#8B7B90', 'textTransform': 'capitalize'}),

                    html.Div([
                        html.P(':'),
                    ], style={'display': 'inline-block', 'textAlign': 'center', 'fontWeight': 'bold'}),

                    html.Div([
                        html.P(str(selected_values[key])),
                    ], style={'textAlign': 'center', 'fontWeight': 'bold', 'color': '#524855',
                              'textTransform': 'capitalize'}),

                ])

            )

        return divs

    return html.Div([' !!! No Current Selections !!!'], style={'font-family': 'Algerian'})


# # ===============================================================================================================

@app.callback(
    Output('selected-values2', 'data'),
    Input('Back', 'n_clicks'),  # prevent_initial_call=True
)
def retrieve_data(n_clicks):
    print('Callback 10 10 10 10 10 10 10')
    global Vendor_selection

    if n_clicks > 0:
        # print('conditions satisfies')
        return Vendor_selection


@app.callback(
    [
        Output('Vendor Supplier_Name', 'options'),
        Output('Vendor Supplier_Name', 'value'),
        Output('Vendor Supplier_Number', 'options'),
        Output('Vendor Supplier_Number', 'value'),
        Output('Vendor Vendor_Prefix', 'options'),
        Output('Vendor Vendor_Prefix', 'value'),
        Output('Vendor GLCLASS', 'options'),
        Output('Vendor GLCLASS', 'value'),
        Output('Vendor Classification', 'options'),
        Output('Vendor Classification', 'value'),
        Output('Vendor Model', 'options'),
        Output('Vendor Model', 'value'),

        Output('Rebate Rebate_Teritory', 'options'),
        Output('Rebate Rebate_Teritory', 'value'),
        Output('Rebate Rebate_Period_From', 'options'),
        Output('Rebate Rebate_Period_From', 'value'),
        Output('Rebate Rebate_Period_TO', 'options'),
        Output('Rebate Rebate_Period_TO', 'value'),
        Output('Rebate Rebate_Frequency', 'options'),
        Output('Rebate Rebate_Frequency', 'value'),
        Output('Rebate Rebate_Currency', 'options'),
        Output('Rebate Rebate_Currency', 'value'),
        Output('Rebate Rebate_Type', 'options'),
        Output('Rebate Rebate_Type', 'value'),

        Output('InputSalesAmount', 'options'),
        Output('InputSalesAmount', 'value'),
        Output('InputRebatesMargin', 'options'),
        Output('InputRebatesMargin', 'value'),
    ],

    [
        Input('selected-values2', 'data')
    ]
)
def retrieve_2(Buffer_data):
    print('Callback 11 11 11 11 11 11')
    global filtered_data, data, Vendor_selection
    global Supplier_Name_1, Supplier_Number_1, Vendor_Prefix_1, GLCLASS_1, Classification_1, Model_1
    global Teritory, Rebate_Period_From, Rebate_Period_TO, Rebate_Frequency, Rebate_Currency, Rebate_Type
    global Slabs, Rebates

    if Buffer_data is not None:
        Vendor_selection = Buffer_data

        if any(Vendor_selection.values()):

            UpdateDataset()
            UpdateVariable()

            return [

                Supplier_Name_1,    Vendor_selection['Vendor Supplier_Name'],
                Supplier_Number_1,    Vendor_selection['Vendor Supplier_Number'],
                Vendor_Prefix_1,    Vendor_selection['Vendor Vendor_Prefix'],
                GLCLASS_1,    Vendor_selection['Vendor GLCLASS'],
                Classification_1,    Vendor_selection['Vendor Classification'],
                Model_1,    Vendor_selection['Vendor Model'],

                Teritory,    Vendor_selection['Rebate Rebate_Teritory'],
                Rebate_Period_From,    Vendor_selection['Rebate Rebate_Period_From'],
                Rebate_Period_TO,    Vendor_selection['Rebate Rebate_Period_TO'],
                Rebate_Frequency,    Vendor_selection['Rebate Rebate_Frequency'],
                Rebate_Currency,    Vendor_selection['Rebate Rebate_Currency'],
                Rebate_Type,    Vendor_selection['Rebate Rebate_Type'],

                Slabs,    Vendor_selection['InputSalesAmount'],
                Rebates,    Vendor_selection['InputRebatesMargin']

            ]

        else:

            filtered_data = data.copy()

            UpdateVariable()

            return [Supplier_Name_1, None, Supplier_Number_1, None, Vendor_Prefix_1, None, GLCLASS_1, None, Classification_1, None, Model_1, None,
                    Teritory, None, Rebate_Period_From, None, Rebate_Period_TO, None, Rebate_Frequency, None, Rebate_Currency, None,
                    Rebate_Type, None, Slabs, None, Rebates, None]

    return [], [], [], [], [], [], [], [], [], [], [], [],    [], [], [], [], [], [], [], [], [], [], [], [],   [], [], [], []


# # ===============================================================================================================

@app.callback(
    [
        Output('Vendor Supplier_Name',  'options',   allow_duplicate=True),
        Output('Vendor Supplier_Number',  'options',   allow_duplicate=True),
        Output('Vendor Vendor_Prefix',  'options',   allow_duplicate=True),
        Output('Vendor GLCLASS',  'options',   allow_duplicate=True),
        Output('Vendor Classification',  'options',   allow_duplicate=True),
        Output('Vendor Model',  'options',   allow_duplicate=True),

        Output('Rebate Rebate_Teritory',  'options',   allow_duplicate=True),
        Output('Rebate Rebate_Period_From', 'options',   allow_duplicate=True),
        Output('Rebate Rebate_Period_TO',  'options',   allow_duplicate=True),
        Output('Rebate Rebate_Frequency',  'options',   allow_duplicate=True),
        Output('Rebate Rebate_Currency',  'options',   allow_duplicate=True),
        Output('Rebate Rebate_Type',  'options',   allow_duplicate=True),

        Output('InputSalesAmount',  'options',   allow_duplicate=True),
        Output('InputRebatesMargin',  'options',   allow_duplicate=True)

    ],

    [
        Input('Vendor Supplier_Name',  'value'),
        Input('Vendor Supplier_Number',  'value'),
        Input('Vendor Vendor_Prefix',  'value'),
        Input('Vendor GLCLASS',  'value'),
        Input('Vendor Classification',  'value'),
        Input('Vendor Model',  'value'),

        Input('Rebate Rebate_Teritory',  'value'),
        Input('Rebate Rebate_Period_From',  'value'),
        Input('Rebate Rebate_Period_TO',  'value'),
        Input('Rebate Rebate_Frequency',  'value'),
        Input('Rebate Rebate_Currency',  'value'),
        Input('Rebate Rebate_Type',  'value'),

        Input('InputSalesAmount',  'value'),
        Input('InputRebatesMargin',  'value'),
       
        State('Rebate Rebate_Teritory',   'value'),
        State('Rebate Rebate_Currency',   'value')
    ], prevent_initial_call=True
)
def value_update(*dropdown_values):
    print('callback 12 12 12 12 12 12 \n')
    global data, Supplier_Name, Supplier_Number, vendor_prefix, GLCLASS, Classification, Model
    global Supplier_Name_1, Supplier_Number_1, Vendor_Prefix_1, GLCLASS_1, Classification_1, Model_1
    global Teritory, Rebate_Period_From, Rebate_Period_TO, Rebate_Frequency, Rebate_Currency, Rebate_Type
    global Vendor_selection, Vendor_Seq_List, Vendor_Var, filtered_data
    global Slabs, Rebates, Teritory_Currency


    rebate_Teritory = dropdown_values[-2]    # first state value
    rebate_Currency = dropdown_values[-1]  
       
    Supplier_Name_1 = Supplier_Number_1 = Vendor_Prefix_1 = GLCLASS_1 = Classification_1 = Model_1 = dash.no_update

    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    triggered_value = dash.callback_context.triggered[0]['value']
   
    print('triggered_id values : ' , triggered_id )
    print('triggered_value  : ' , triggered_value )

    if dash.callback_context.triggered and triggered_value :

        if triggered_id.split()[0] == 'Vendor' and len(triggered_value) > 0:

            Vendor_selection[triggered_id] = triggered_value

            variable_names = ['Supplier_Name_1', 'Supplier_Number_1', 'Vendor_Prefix_1', 'GLCLASS_1', 'Classification_1', 'Model_1',
                              'Teritory_1', 'Rebate_Period_From_1', 'Rebate_Period_TO_1', 'Rebate_Frequency_1', 'Rebate_Currency_1', 'Rebate_Type_1']

            if triggered_id not in Vendor_Seq_List:
                print('Selection is going forward')
               
                if triggered_value and triggered_id not in Vendor_Seq_List:
                    Vendor_Seq_List.append(triggered_id)

                temp = list(set(filtered_data[triggered_id.split()[1]]))
               
                UpdateDataset()
                UpdateVariable()
                               
                if "SELECT_ALL" in triggered_value:
                    globals()[variable_names[variable_names.index(str(triggered_id.split()[1])+'_1')]] = ['SELECT_ALL']
                else:
                    globals()[variable_names[variable_names.index(str(triggered_id.split()[1])+'_1')]] = temp
                   
            else:

                temp = None
                print('Selection is going Backward')

                filtered_data = data.copy()
                               
                for i in Vendor_Seq_List:
                    if Vendor_selection[i] is not None and len(Vendor_selection[i]) > 0:
                        if "SELECT_ALL" in Vendor_selection[i]:
                            # print('condition 1')
                            Vendor_selection[i] = ['SELECT_ALL']
                            continue
                        else:
                            filtered_data = filtered_data[filtered_data[i.split()[1]].isin(Vendor_selection[i])]
                            Vendor_Var = Vendor_Seq_List.index(i)

                        if (Vendor_Seq_List.index(i) + 1) == (Vendor_Seq_List.index(triggered_id)):

                            temp = list(set(filtered_data[triggered_id.split()[1]]))

                if temp is None:
                    temp = list(set(data[triggered_id.split()[1]]))

                # filtered_data = filtered_data.copy()
                filtered_data.loc[len(filtered_data)] = "SELECT_ALL"
               
                temp.append('SELECT_ALL')

                # print('filtered_data values are :::::::::' , filtered_data)                

                UpdateVariable()

                if "SELECT_ALL" in triggered_value:
                    globals()[variable_names[variable_names.index(str(triggered_id.split()[1])+'_1')]] = ['SELECT_ALL']
                else:
                    globals()[variable_names[variable_names.index(str(triggered_id.split()[1])+'_1')]] = temp
                    globals()[variable_names[variable_names.index(str(triggered_id.split()[1])+'_1')]] = list(set(globals()[variable_names[variable_names.index(str(triggered_id.split()[1])+'_1')]]))
                   
        elif (triggered_id.split()[0] == 'Rebate' or 'Input' in triggered_id.split()[0]) and len(triggered_value) > 0:
            Vendor_selection[triggered_id] = triggered_value

            if triggered_id.split()[-1] == 'Rebate_Teritory':
                if len(rebate_Teritory) > 0:
                    Rebate_Currency = []
                    for i in rebate_Teritory:
                        Rebate_Currency.append(Teritory_Currency[Teritory_Currency.index(i)+1])  

            elif triggered_id.split()[-1] == 'Rebate_Currency':
                if len(rebate_Currency) > 0:
                    Teritory = []
                    for i in rebate_Currency:
                        Teritory.append(Teritory_Currency[Teritory_Currency.index(i)-1])

        else:
            if not rebate_Teritory:
                Teritory = sorted(list(set(data2['Rebate_Teritory'])), key=lambda x: (isinstance(x, str), x), reverse=True)
            if not rebate_Currency:
                Rebate_Currency = sorted(list(set(data2['Rebate_Currency'])), key=lambda x: (isinstance(x, str), x), reverse=True)

            Vendor_selection[triggered_id] = None
            filtered_data = data.copy()

            UpdateDataset()
            UpdateVariable()

        return [
            Supplier_Name_1, Supplier_Number_1, Vendor_Prefix_1, GLCLASS_1, Classification_1, Model_1,
            Teritory, Rebate_Period_From, Rebate_Period_TO, Rebate_Frequency, Rebate_Currency, Rebate_Type,
            Slabs, Rebates
        ]
   
    else:
        print('conditino satisifies')
       
        if 'Vendor' in triggered_id:
            if triggered_id in Vendor_Seq_List:
                Vendor_Seq_List.remove(triggered_id)
        elif 'Rebate_' in triggered_id:
            Teritory = sorted(list(set(data2['Rebate_Teritory'])), key=lambda x: (isinstance(x, str), x), reverse=True)
            Rebate_Currency = sorted(list(set(data2['Rebate_Currency'])), key=lambda x: (isinstance(x, str), x), reverse=True)            
       
        filtered_data = data.copy()
       
        UpdateDataset()
        UpdateVariable()
       
        # print('filtered_data values are ::::::::::::' , filtered_data)

    return [
          Supplier_Name_1, Supplier_Number_1, Vendor_Prefix_1, GLCLASS_1, Classification_1, Model_1,
          Teritory, Rebate_Period_From, Rebate_Period_TO, Rebate_Frequency, Rebate_Currency, Rebate_Type,
          Slabs, Rebates
      ]

app.run_server(debug=False, host="0.0.0.0")

#app.run_server(debug=True)
