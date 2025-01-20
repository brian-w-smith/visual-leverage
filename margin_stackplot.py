"""
Visually explain leverage / margin loans.
Demonstrates difference between simple interest compared to compounding effects of capital gain.
Margin interest payment is assumed to be calculated as simple interest, i.e. no compounding

"""

import matplotlib.pyplot as plt
import numpy as np
import sympy as sym
from matplotlib.widgets import Button, Slider, TextBox, RadioButtons


title = 'Visual Margin'
x_ticks = 12
month_index = np.linspace(0, x_ticks, num=x_ticks)

cagr = .05 #compound annual growth rate
cost_of_capital = .12 #Loan interest, varies by bank.
maintenance_requirement = .3 # 30% is standard. AKA collateral

equity = 100000.0
loan_amount = 0.0
pay_interest_with_wages = False # The margin loan interest payments can be paid by selling equities, or injecting capital from an external account

text = "The margin amount is {:3,.2}.\nThe monthly interest payment is {:3,.2}."




## Plot arrangement 

fig = plt.figure(layout='constrained', figsize=(10,5))
ax_dict = fig.subplot_mosaic(
    [
        ['equity', 'plot', 'plot'],
        ['margin_ratio', 'plot', 'plot'],
        ['gainloss_slider', 'plot', 'plot'],
        ['maint', 'plot', 'plot'],
        ['interest', 'plot', 'plot'],
        ['months', 'text', 'text'],
        ['payment_radio', 'text', 'text']
    ])

fig.canvas.manager.set_window_title(title)
ax_dict['text'].set_axis_off()
ax_dict['text'].text(0,0, text.format( int(loan_amount*100)/100,  int(loan_amount * cost_of_capital / 12*100)/100 ))



## Left Controls 


equity_box = TextBox(ax_dict['equity'], "Starting Equity")
equity_box.set_val(str(equity))
margin_ratio_slider = Slider(
    ax=ax_dict['margin_ratio'],
    label="Margin Equity %",
    valmin=0,
    valmax=0.5,
    valinit=0,
    orientation="horizontal",
    valfmt='%.2f'
)
gainloss_slider = Slider(
    ax=ax_dict['gainloss_slider'],
    label="Annualized Rate of Return",
    valmin=-.99,
    valmax=2.0,
    valinit=cagr,
    orientation="horizontal",
    valfmt='%.2f'
)
maint_box = TextBox(ax_dict['maint'], "Maintenance Requirement")
maint_box.set_val(str(maintenance_requirement))
interest_box = TextBox(ax_dict['interest'], "Interest Rate")
interest_box.set_val(str(cost_of_capital))
total_months_box = TextBox(ax_dict['months'], "Total Months")
total_months_box.set_val(str(x_ticks))
payment_radio_labels = ['Pay Interest with Equity', 'Pay Interest with Outside Income (Wages)']
payment_radio_button = RadioButtons(ax_dict['payment_radio'], payment_radio_labels, active= int(pay_interest_with_wages))



#Math


def calc(x_ticks, cagr, cost_of_capital, loan_amount, equity, pay_interest_with_wages):
    if pay_interest_with_wages:
        ay_lambda = lambda i,j: equity * (1.0+cagr) ** (j/12.0)
    else:
        ay_lambda = lambda i,j: equity * (1.0+cagr) ** (j/12.0) - ( j * loan_amount * cost_of_capital / 12.0)

    ay = np.fromfunction(ay_lambda, (1,x_ticks)) 
    by = np.fromfunction(lambda i,j: loan_amount * (1.0+cagr) ** (j/12.0), (1,x_ticks))
    y = np.vstack([ay, by])
    return y

def check_margin_call(data, maintenance_requirement, loan_amount):
    for i, mv in enumerate(data[0]):
        equity_total = mv+data[1][i]
        equity_percent = (equity_total-loan_amount)/equity_total
        if equity_percent < maintenance_requirement:
            return i
    return -1


def update(val = 0 ):
    ax_dict['plot'].clear()
    x_ticks = int(total_months_box.text ) 
    month_index = np.linspace(0, x_ticks, num=x_ticks)
    cagr = gainloss_slider.val
    cost_of_capital = float(interest_box.text)
    equity = float(equity_box.text)
    x = sym.symbols('x')
    eq = sym.Eq(x/(x+equity)-margin_ratio_slider.val, 0.0)
    sol = sym.solve(eq, x)
    loan_amount = float(sol[0]) 
    maintenance_requirement = float(maint_box.text)
    pay_interest_with_wages = payment_radio_button.index_selected == 1

    data = calc(x_ticks, cagr, cost_of_capital, loan_amount, equity, pay_interest_with_wages)
    margin_call_index = check_margin_call(data, maintenance_requirement, loan_amount)
    if margin_call_index > -1:
        mid_x = int(x_ticks/2.0) # cast to int since its used as an index
        mid_y = (data[0][mid_x]+data[1][mid_x])/2
        ax_dict['plot'].annotate('margin call \nat month '+str(margin_call_index), xy=(mid_x,mid_y))
    poly = ax_dict['plot'].stackplot(month_index, data)
    poly[0].set_label('Your Equity')
    poly[1].set_label('Margin Equity')
    for i in range(x_ticks):
        if (i%(x_ticks/4)==0.0):
            equity_total = data[0][i]+data[1][i]
            equity_percent = (equity_total-loan_amount)/equity_total
            ax_dict['plot'].annotate('{0:.2}'.format(equity_percent), xy=(i, data[0][i]))
    ax_dict['plot'].set_xlabel('Months')
    ax_dict['plot'].set_ylabel('Portfolio Market Value')
    ax_dict['plot'].legend()
    fig.canvas.draw_idle()
    ax_dict['text'].clear()
    ax_dict['text'].set_axis_off()
    ax_dict['text'].text(0,0, text.format(loan_amount, loan_amount * cost_of_capital / 12.0 ))


equity_box.on_submit(update)
margin_ratio_slider.on_changed(update)
gainloss_slider.on_changed(update)
maint_box.on_submit(update)
total_months_box.on_submit(update)
interest_box.on_submit(update)
payment_radio_button.on_clicked(update)

update()
plt.show()



