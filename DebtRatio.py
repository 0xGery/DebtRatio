import numpy as np
from scipy.optimize import fsolve

def calculate_new_price(NewPrice, LiquidityUSDC, Pb, NewBorrowedETHValue, DebtRatioTarget):
    # Recalculate ETH on Uniswap with the new price
    ETHonUniswap_new = LiquidityUSDC * ((np.sqrt(Pb) - np.sqrt(NewPrice)) / (np.sqrt(NewPrice) * np.sqrt(Pb)))
    ETHonUniswapValue_new = ETHonUniswap_new * NewPrice

    # Recalculate the debt ratio
    DebtRatio_new = (NewBorrowedETHValue / ETHonUniswapValue_new) - 1

    return DebtRatio_new - DebtRatioTarget

# parameters input
TotalDeposit = float(input("Total Deposit in USDC: "))
CurrentPrice = float(input("Current ETH Price in USDC: "))
RangeSpread = float(input("Range Spread as a decimal (e.g., 0.15 for 15%): "))
debt_ratio_plus = float(input("target positive debt ratio (e.g., 0.075 for +7.5%): "))

# Calculate the negative debt ratio
debt_ratio_minus = -debt_ratio_plus

# Calculate LowerTick and UpperTick
Pa = CurrentPrice - (CurrentPrice * RangeSpread)
Pb = CurrentPrice + (CurrentPrice * RangeSpread)

# Deposit & Lend on Aave
AaveCollateral = TotalDeposit / 1.65
ETHBorrowValue = AaveCollateral * 0.65

# LPing to Uniswap V3
AllocatedUSDC = TotalDeposit - AaveCollateral
LiquidityUSDC = AllocatedUSDC / (np.sqrt(CurrentPrice) - np.sqrt(Pa))
ETHonUniswap = LiquidityUSDC * ((np.sqrt(Pb) - np.sqrt(CurrentPrice)) / (np.sqrt(CurrentPrice) * np.sqrt(Pb)))
ETHonUniswapValue = ETHonUniswap * CurrentPrice

# Repay Debt on Aave
unUsedETH = ETHBorrowValue - ETHonUniswapValue
NewBorrowedETHValue = ETHBorrowValue - unUsedETH

# Initial Debt Ratio (should be 0)
DebtRatio_initial = (NewBorrowedETHValue / ETHonUniswapValue) - 1

# Output initial calculation details
print("\nInitial Calculations:")
print("pa:", Pa)
print("pa:", Pb)
print("AaveCollateral:", AaveCollateral)
print("ETHBorrowValue:", ETHBorrowValue)
print("AllocatedUSDC:", AllocatedUSDC)
print("LiquidityUSDC:", LiquidityUSDC)
print("ETHonUniswap:", ETHonUniswap)
print("ETHonUniswapValue:", ETHonUniswapValue)
print("unUsedETH:", unUsedETH)
print("NewBorrowedETHValue:", NewBorrowedETHValue)
print("Initial Debt Ratio:", DebtRatio_initial)

# Solving for the new prices for specified debt ratios
new_price_plus = fsolve(calculate_new_price, CurrentPrice, args=(LiquidityUSDC, Pb, NewBorrowedETHValue, debt_ratio_plus))[0]
new_price_minus = fsolve(calculate_new_price, CurrentPrice, args=(LiquidityUSDC, Pb, NewBorrowedETHValue, debt_ratio_minus))[0]

# Output final results
print("\nFinal Results:")
print("New Price for +7.5% Debt Ratio:", new_price_plus)
print("New Price for -7.5% Debt Ratio:", new_price_minus)
