import pyperclip as pc
def all():
    s = '''1:
linear
ft
parabola
elast
mape
mae
2:
ramsey
homo
remove_hetero
avto
vif
3:
prognoz
doverit
'''
    return pc.copy(s)
def ft():
    s = '''#F критерий (0.05, k1 (число факторов), k2 (число набл. - факторов - 1))
#t табл (0.05, n - 1)
'''
    return pc.copy(s)
def linear():
    s = '''import statsmodels.api as sm
X = np.array([1.9,1.1,4.7,4.9,1.2,1.8,2.7,2.7,4.9,2.5,3.6,3.5,2.9,1,2,3.6,3.5])
Y = np.array([9.57,3.15,3.87,1.13,1.45,8.78,6.99,6.4,7.82,6.11,2.49,4.75,5.19,9.82,2.77,2.49,4.75])
X = sm.add_constant(X)
model = sm.OLS(Y, X).fit()
# Результаты F-теста Фишера
f_test = model.fvalue, model.f_pvalue
# Результаты t-теста Стьюдента для каждого коэффициента
t_test = model.tvalues, model.pvalues
# Интервальные оценки для параметров модели
conf_intervals = model.conf_int()
# Коэффициент детерминации (R-квадрат)
r_squared = model.rsquared'''
    return pc.copy(s)
    
def parabola():
    s = '''import statsmodels.api as sm
import statsmodels.formula.api as smf
#Параболическая
X2 = X**2
quadratic_model = sm.OLS(Y, sm.add_constant(np.column_stack((X, X2)))).fit()
print("Квадратичная модель:\n", quadratic_model.summary())
# Экспоненциальная. Логарифмирование Y
Y_log = np.log(Y)
exp_model = sm.OLS(Y_log, sm.add_constant(X)).fit()
print("Экспоненциальная модель:\n", exp_model.summary())
# Степенная. Логарифмирование X и Y
X_log = np.log(X)
Y_log = np.log(Y)
power_model = sm.OLS(Y_log, sm.add_constant(X_log)).fit()
print("Степенная модель:\n", power_model.summary())'''
    return pc.copy(s)
    
def elast():
    s = '''#строим модель
beta_0, beta_1 = model.params
#Средние значения
X_mean = np.mean(X[:, 1])
Y_mean = np.mean(Y)
elasticity = beta_1 * (X_mean / Y_mean)
#Дельта-коэффициент (коэффициент наклона)
delta = beta_1
Если, например, elasticity равен 0.8, это означает,
что процентное изменение в  X приведет к 0.8-кратному процентному
изменению в Y в среднем. 
Если delta равен 1.5, это означает, что изменение 
X на одну единицу приведет в среднем к изменению 
Y на 1.5 единиц
В случае множественной регрессии дельта-коэффициенты по-прежнему интерпретируются
как мера абсолютного изменения зависимой переменной в ответ
на изменение каждой отдельной независимой переменной, но при условии,
что все остальные переменные в модели остаются постоянными'''
    return pc.copy(s)

def mape():
    s = '''y_true = np.array([3, 2, 5, 7])
y_pred = np.array([2.5, 2.1, 4.8, 7.2])
mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
print("Средняя относительная ошибка аппроксимации (MAPE):", mape, "%")'''
    return pc.copy(s)
    
def mae():
    s = '''mae = np.mean(np.abs(y_true - y_pred))
print(mae) 
'''
    return pc.copy(s)
    
def prognoz():
    s = '''#Точечный прогноз
model = sm.OLS(y, sm.add_constant(x)).fit()
X_max_110 = np.max(X) * 1.10
point_forecast_110 = model.predict([1, X_max_110])
X_mean = np.mean(X)
point_forecast_mean = model.predict([1, X_mean])
#Интервальный
from statsmodels.sandbox.regression.predstd import wls_prediction_std
# Интервальный прогноз для 110% от максимального значения X
pred_std_110, interval_l_110, interval_u_110 = wls_prediction_std(model, exog=np.array([[1, X_max_110]]), alpha=0.05)
# Интервальный прогноз для среднего значения X
pred_std_mean, interval_l_mean, interval_u_mean = wls_prediction_std(model, exog=np.array([[1, X_mean]]), alpha=0.05)
'''
    return pc.copy(s)

def doverit():
    s = '''X = sm.add_constant(X)
model = sm.OLS(Y, X).fit()
conf_intervals = model.conf_int(alpha=0.05)
conf_intervals
'''
    return pc.copy(s)
    
def ramsey():
    s = '''#Тест Рамсея на проверку пропущенных переменных    
#Если p-value < 0.05, то неправлильная спецификация модели, могут быть пропущены переменные    
#Если p-value > 0.05, то нет оснований отвергать нулевую гипотезу о том, что модель правильно специфицирована, нет достаточных доказательств для того, чтобы утверждать о присутствии проблем в спецификации модели.
from statsmodels.stats.outliers_influence import reset_ramsey
xc = sm.add_constant(x)
model = sm.OLS(y, xc).fit()
reset_test = reset_ramsey(model, degree=3)
print(reset_test)'''
    return pc.copy(s)
    
def homo():
    s = '''#Если p-значение < 0.05, это указывает на наличие гетероскедастичности в остатках модели. 
#Это означает, что остатки не являются гомоскедастичными, и стандартные ошибки коэффициентов модели могут быть недооценены,
#что ведет к неверным выводам о статистической значимости коэффициентов. 
#Если p > 0.05, это предполагает, что остатки модели вероятно гомоскедастичны.
from statsmodels.stats.diagnostic import het_breuschpagan
residuals = model.resid
bp_test = het_breuschpagan(residuals, model.model.exog)
print('BP statistic: ', bp_test[0])
print('p-value: ', bp_test[1])'''
    return pc.copy(s)

def remove_hetero():
    s = '''#Устранение гетероскедастичности
#1) Преобразование y
# Логарифмическое преобразование Y
Y_transformed = np.log(Y)
# Повторное построение модели с преобразованной Y
model = sm.OLS(Y_transformed, X).fit()

#2) Преобразование X
# преобразование X, если это имеет смысл с точки зрения вашего анализа
X_transformed = np.sqrt(X)
# Построение модели с преобразованными X
model = sm.OLS(Y, X_transformed).fit()

#или
X_log_transformed = np.log(X + 1)  # Добавляем 1 для избежания log(0)
# Построение модели с логарифмированными независимыми переменными
model = sm.OLS(Y, sm.add_constant(X_log_transformed)).fit()
'''
    return pc.copy(s)
    
def avto():
    s = '''#Значение около 2 указывает на отсутствие автокорреляции.    
#Значения ближе к 0 указывают на положительную автокорреляцию.    
#Значения ближе к 4 указывают на отрицательную автокорреляцию.
from statsmodels.stats.stattools import durbin_watson
test = durbin_watson(model.resid)
print(test)'''
    return pc.copy(s)
    
def vif():
    s = '''Если VIF > 3, значит мультиколлинеарность есть
from statsmodels.stats.outliers_influence import variance_inflation_factor
X = sm.add_constant(x)
# Вычисление VIF для каждой переменной
# X должен быть DataFrame с признаками
vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)'''
    return pc.copy(s)
