weight = 1.5
# Ground shipping
if weight <= 2:
  cost_g_ship = weight * 1.5 + 20
elif weight >= 2 and weight <= 6:
  cost_g_ship = weight * 3.00 + 20
elif weight >= 6 and weight <= 10:
  cost_g_ship = weight * 4.00 + 20
elif weight > 10:
  cost_g_ship = weight * 4.75 + 20
cost_g_ship_premium = 120.00
print("Ground Shipping cost premium: $",cost_g_ship_premium)
# Drone Shipping
if weight <= 2:
  cost_d_shipping = weight * 4.50 + 0
elif weight >= 2 and weight <= 6:
  cost_d_shipping = weight * 9.00 + 0
elif weight >= 6 and weight <= 10:
  cost_d_shipping = weight * 12.00 + 0
elif weight > 10:
  cost_d_shipping = weight * 14.25 + 0
