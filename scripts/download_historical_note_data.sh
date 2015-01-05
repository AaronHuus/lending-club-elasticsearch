#!/bin/sh
echo "Time to download some data!"
mkdir -p ../historical_data
cd ../historical_data
rm LoanStats3*
rm RejectStats*
rm LCDataDictionary.xlsx

wget https://resources.lendingclub.com/LCDataDictionary.xlsx

wget https://resources.lendingclub.com/LoanStats3a_securev1.csv.zip
unzip LoanStats3a_securev1.csv.zip
sed -i '' '1d' LoanStats3a_securev1.csv
sed -i '' '$d' LoanStats3a_securev1.csv
sed -i '' '$d' LoanStats3a_securev1.csv
sed -i '' '/Loans that do not meet the credit policy/d' LoanStats3a_securev1.csv
# Deletes empty lines
sed -i ''  '/^$/d' LoanStats3a_securev1.csv

wget https://resources.lendingclub.com/LoanStats3b_securev1.csv.zip
unzip LoanStats3b_securev1.csv.zip
sed -i '' 's/Infinity/Infinite/' LoanStats3b_securev1.csv
sed -i ''  's/infinity/infinite/' LoanStats3b_securev1.csv
sed -i '' '1d' LoanStats3b_securev1.csv
sed -i '' '$d' LoanStats3b_securev1.csv
sed -i '' '$d' LoanStats3b_securev1.csv
sed -i '' '/^$/d' LoanStats3b_securev1.csv

wget https://resources.lendingclub.com/LoanStats3c_securev1.csv.zip
unzip LoanStats3c_securev1.csv.zip
sed -i '' '1d' LoanStats3c_securev1.csv
sed -i '' '$d' LoanStats3c_securev1.csv
sed -i '' '$d' LoanStats3c_securev1.csv
sed -i '' '/^$/d' LoanStats3c_securev1.csv

wget https://resources.lendingclub.com/RejectStatsA.csv.zip
unzip RejectStatsA.csv.zip
sed -i '' '1d' RejectStatsA.csv

wget https://resources.lendingclub.com/RejectStatsB.csv.zip
unzip RejectStatsB.csv.zip
sed -i '' '1d' RejectStatsB.csv

rm *.zip
