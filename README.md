
**Purpose :**

Finding reorder level, safety stock, generate demand and visualize the results for two different service level and lead times.

**How it works :**

The program takes following as input values.

* "sample size " as days for the desired time horizon.
* Mean and deviation of the demand values to be generated.
* Replenishment size as reorder quantity
* Two lead times
* Two service rates

Once the inputs are loaded the program will generate four different demand array of length sample size for combinations of lead times and service rates.

Then calculates the the different inventory levels.

The outputs are displayed in the terminal and subsequently their copies were saved to Order.xlsx file store in local directory.

Finally a graphical visualization of four demands as plots shown.

Alternatively use app.py for GUI in html.


**Dependent Libraries :**

* matplotlib
* numpy
* scipy
* math
* pandas
* openpyxl
* tabulate
* base64
* io
* flask

**Author :**

    Dipson
