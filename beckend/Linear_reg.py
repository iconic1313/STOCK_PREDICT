# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression

# x=np.array([1,2,3,4,5]).reshape(-1, 1)
# y=np.array([2,4,3,5,6])

# model =LinearRegression()
# model.fit(x,y)

# y_pred = model.predict(x)
 
# print("co-efficiet", model.coef_[0])

# plt.scatter(x,y,color='blue',label='')
# plt.plot(x, y_pred, color='red', label='Predicted')
# plt.title('Linear Regression Example')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.show()


import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

sqr =np.array([100,400,600,2000]).reshape(-1, 1)
price=np.array([12,30,50,150])

model=LinearRegression()
model.fit(sqr,price)

pred_val=model.predict([[1600]])
print ("coefficient",model.coef_[0])
print(f"predicted price for 1200 is {pred_val[0]:.2f} lakhs ")
 
plt.scatter(sqr, price, color='blue', label='Actual Prices')
plt.plot(sqr, model.predict(sqr), color='red', label='Regression Line')
plt.scatter([1200], pred_val, color='green', marker='x', s=100, label='Predicted (1200 sq ft)')

plt.title('Linear Regression Example')
plt.xlabel('squere feet')
plt.ylabel('price in lakhs')
plt.show()

