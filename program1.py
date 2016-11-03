import time

start_time = time.clock()

#enumeration fuction
def enumeration(array):
	maxarray = 0

	for i in range(len(array)):
		for j in range(i, len(array)):

			maxArraySum = sum(array[i:j+1])


			if maxArraySum > maxarray:
				maxarray = maxArraySum
				start = i
				finish = j

	mss = array[start:finish+1]

	return {'MAXARR':maxarray, 'MAXSUB':mss}


#better enumeration function
def betterEnumeration(arr):
	maxarr = 0
	start = finish = 0

	for i in range(len(arr)):
		maxarrSum = 0

		for j in range(i, len(arr)):
			maxarrSum += arr[j]


			if maxarrSum > maxarr:
				maxarr = maxarrSum
				start = i
				finish = j

	mss2 = arr[start:finish+1]

	return {'MAXARRAY':maxarr, 'MAXSUBARR':mss2}


def algorithm3 (array, low, high):

	if(low == high):
		return array[low]

	middle = (low+high)//2
	leftAns = algorithm3(array, low, middle)
	rightAns = algorithm3(array, middle+1, high)
	leftMax = array[middle]
	rightMax = array[middle+1]
	temp = 0

	for x in range(middle, low, -1):
		temp += array[x]
		if temp > leftMax:
			leftMax = temp
	temp = 0
	for x in range(middle+1, len(array)):
		temp += array[x]
		if (temp > rightMax):
			rightMax = temp

	return max(max(leftAns, rightAns), leftMax+rightMax)

def alg4(arr):
	maxSum = -1
	endHereSum = -1
	endHereLow = 0
	endHereHigh = 0
	low = 0
	high = 0
	index = 0
	for num in arr:
		endHereHigh = index
		if endHereSum > 0:
			endHereSum = endHereSum + num
		else:
			endHereLow = index
			endHereSum = num
		if endHereSum > maxSum:
			maxSum = endHereSum
			low = endHereLow
			high = endHereHigh
		index += 1
	return {'LOW':low, 'HIGH':high, 'SUBSUM':maxSum, 'SUBARR':arr[low:(high + 1)]}

f = open('MSS_Problems.txt', 'r')
f1 = open('MSS_Results.txt', 'w')

for line in f:
	newData = line.replace("[", "", 1)
	newData = newData.replace("]", "", 1)

	if len(line) > 3:
		parsed = [int(el) for el in newData.split(',')]


	if len(parsed) == 0:
		print "Length of input array zero"

	f1.write("Enumeration\n")
	f1.write("Array Processed: \n" + str(parsed) + "\n")
	maximum1 = enumeration(parsed)
	f1.write("Maximum sum: \n" + str(maximum1['MAXARR']) + "\n")
	f1.write("Maximum subarray: \n" + str(maximum1['MAXSUB']) + "\n\n")

	f1.write("Better Enumeration\n")
	f1.write("Array Processed: \n" + str(parsed) + "\n")
	maximum2 = betterEnumeration(parsed)
	f1.write("Maximum sum: \n" + str(maximum2['MAXARRAY']) + "\n")
	f1.write("Maximum subarray: \n" + str(maximum2['MAXSUBARR']) + "\n\n")

	f1.write("Divide and Conquer\n")
	f1.write("Array Processed: \n" + str(parsed) + "\n")
	maximum3 = algorithm3(parsed, 0, len(parsed)-1)
	f1.write("Maximum sum: \n" + str(maximum3) + "\n")
	f1.write("Maximum subarray: \n" + str(maximum1['MAXSUB']) + "\n\n")

	f1.write("Dynamic Array\n")
	f1.write("Array Processed: \n" + str(parsed) + "\n")
	maximum4 = alg4(parsed)
	f1.write("Maximum sum: \n" + str(maximum4['SUBSUM']) + "\n")
	f1.write(("Max subarray: \n") + str(maximum4['SUBARR']) + "\n\n")


f.close()
f1.close()