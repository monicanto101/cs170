import math

# open data sets
def mkDataSet(fileName):
	data_set = []
	with open(fileName) as f:
		for i in f.readlines():
			try:
				temp = i.lstrip("  ")
				temp = [float(j) for j in temp.split()]
				temp[0] = int(temp[0])
				data_set.append(temp)
			except ValueError as e:
				print("error",e,"on line", i)
	return data_set

# normalization
def normalize(active_data_set):
	data_set = active_data_set
	avg = [0.00] * (len(data_set[0]) - 1)
	std_dev = [0.00] * (len(data_set[0]) - 1)
	# averages
	for i in data_set:
		for j in range (1,(len(i))):
			avg[j - 1] = avg[j - 1] +  i[j]
	for i in range(len(avg)):
		avg[i] = (avg[i] / len(data_set))
	# standard deviation 
	# sigma = sqrt((sum(x - mean)^2) / n)
	for i in data_set:
		for j in range (1, (len(i))):
			std_dev[j - 1] = std_dev[j - 1] + pow((i[j] - avg[j - 1]), 2)
	for i in range(len(std_dev)):
		std_dev[i] = math.sqrt(std_dev[i] / len(data_set))
	# new values 
	# new_values = (x - mean) / standard deviation
	for i in range(len(data_set)):
		for j in range (1, (len(data_set[0]))):
			data_set[i][j] = (data_set[i][j] - avg[j - 1]) / std_dev[j - 1]
	return data_set

# similarity
def distance(a, b, params): 
	dist = 0
	for i in range(len(params)):
		if params[i]:
			dist += pow((a[i] - b[i]), 2) # dist = dist + pow((a[i] - b[i]), 2)
	return math.sqrt(dist)

# find k-nearest neighbors (KNN)
import operator 
def get_neighbor(training_set, test_instance, k, params):
	dis = []
	for x in range(len(training_set)):
		dist = distance(test_instance, training_set[x], params)
		dis.append((training_set[x], dist))
	dis.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(dis[x][0])
	return neighbors

# compute accuracy
# multiply by 100 for percentage
def get_accuracy(data_set, flags):
	acc = 0.00
	for i in range(len(data_set)):
		training_set = list(data_set)
		test_instance = training_set.pop(i) 
		neighbors = get_neighbor(training_set, test_instance, 1, flags)
		if (len(neighbors) == 1):
			if (neighbors[0][0] == test_instance[0]):
				acc = acc + 1
	acc = (acc / len(data_set)) * 100
	return acc

# forward selection
# input: empty features, accuracy
# output: best features, best accuracy
def get_forward_feature_set(data_set, possible_flags, current_features, best_acc):
	acc = 0.0
	flags_left = [i for i in possible_flags if i not in current_features]
	flag_scores = [0.0] * len(flags_left)
	current_index = 0
	for i in flags_left:
		flags = [0] * (len(possible_flags) + 1)
		flags[i] = 1
		for j in current_features:
			flags[j] = 1
		acc = get_accuracy(data_set, flags)
		flag_scores[current_index] = acc
		feature_set = list(current_features)
		feature_set.append(i)
		print("Using feature(s) {", end=' ')
		if (len(feature_set) == 1):
			print(feature_set[0], end=' ')
		else:
			print(','.join(str(i) for i in feature_set), end=' ')
		print("} accuracy is ",flag_scores[current_index],"%")
		current_index = current_index + 1
	feature_set = list(current_features)
	y = max(flag_scores)
	for i in range(len(flags_left)):
		if (flag_scores[i] == y):
			feature_set.append(flags_left.pop(i))
			break
	print("\n")
	if(y < best_acc):
		print("(Warning, Accuracy has decreased!", end=' ')
		print("Continuing search in case of local maxima)", end=' ')
	print("\nFeature set {", end=' ')
	if (len(feature_set) == 1):
		print(feature_set[0], end=' ')
	else:
		print(','.join(str(i) for i in feature_set), end=' ')
	print("} was best, accuracy is ", y,"%\n")
	return (feature_set, y)

# backward elimination
# input: existing features, accuracy
# output: best features, best accuracy
def get_backward_feature_set(data_set, possible_flags, current_features, best_acc):
	acc = 0.0
	flags_left = list(current_features)
	flag_scores = [0.0] * len(flags_left)
	current_index = 0
	for i in flags_left:
		flags = [0] * (len(possible_flags) + 1)
		for j in current_features:
			flags[j] = 1
		flags[i] = 0
		acc = get_accuracy(data_set, flags)
		flag_scores[current_index] = acc
		feature_set = list(current_features)
		feature_set.remove(i)
		print("Using feature(s) {", end=' ')
		if (len(feature_set) == 1):
			print(feature_set[0], end=' ')
		else:
			print(','.join(str(i) for i in feature_set), end=' ')
		print("} accuracy is ",flag_scores[current_index],"%")
		current_index = current_index + 1
	feature_set = list(current_features)
	y = max(flag_scores)
	useless_link = 0
	for i in range(len(flag_scores)):
		if (flag_scores[i] == y):
			useless_link = flags_left.pop(i)
			feature_set.remove(useless_link)
			break
	if(y < best_acc):
		print("\n(Warning, Accuracy has decreased!", end=' ')
		print("Continuing search in case of local maxima)", end=' ')
	print("\nFeature set {", end=' ')
	if (len(feature_set) == 1):
		print(feature_set[0], end=' ')
	else:
		print(','.join(str(i) for i in feature_set), end=' ')
	print("} was best, removing ",useless_link," has the highest accuracy,", y,"%\n")
	return (feature_set, y)

# pruning	
# input: data set, sorted scores, accuracy
# output: best features, best accuracy
def get_special_feature_set(data_set, sorted_scores, best_acc):
	acc = 0.0
	flags_left = [i[1] for i in sorted_scores]
	current_best_acc = best_acc
	current_best_feat = [flags_left[-1]]
	flag_scores = [0.0] * len(flags_left)
	current_index = 0
	flags = [0] * (len(flags_left) + 1)
	for i in range(len(flags_left)):
		flags[flags_left[len(flags_left) - i - 1]] = 1
		acc = get_accuracy(data_set, flags)
		flag_scores[current_index] = acc
		feature_set = flags_left[(len(flags_left) - i - 1):]
		if (acc > current_best_acc):
			current_best_acc = acc
			current_best_feat = list(feature_set)
		print("Using feature(s) {", end=' ')
		if (len(feature_set) == 1):
			print(feature_set[0], end=' ')
		else:
			print(','.join(str(i) for i in feature_set), end=' ')
		print("} accuracy is ",flag_scores[current_index],"%")
		current_index = current_index + 1
	y = max(flag_scores)
	for i in range(len(flags_left)):
		if (flag_scores[i] == y):
			feature_set = flags_left[len(flags_left) - i - 1:]
			break
	print("\nFeature set {", end=' ')
	if (len(feature_set) == 1):
		print(feature_set[0], end=' ')
	else:
		print(','.join(str(i) for i in feature_set), end=' ')
	print("} was best, accuracy is ", y,"%\n")
	return (current_best_feat, current_best_acc)

def forward(fileName):
	data_set = mkDataSet(fileName)
	instances = len(data_set)
	features = len(data_set[0]) - 1
	print("\nThis dataset has ",features," features (not including the class attribute), with "\
	,instances," instances.\n")
	# print("Normalizing data...", end=' ')
	# call normalize
	data_set = normalize(data_set)
	# print("Done!")
	flags = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	# call get_accuracy
	acc = get_accuracy(data_set, flags)
	print("Running nearest neighbor with all "\
	 ,features," features, using \"leaving-one-out\" evaluation, I get an accuracy of "\
	 ,acc,"%\n")
	print("Beginning search.\n")
	pos_flags = [i for i in range(1, features + 1)]
	feature_set = []
	best_feat_set = []
	best_acc = 0.0
	for i in range(features):
		return_val = get_forward_feature_set(data_set, pos_flags, feature_set, best_acc)
		feature_set = return_val[0]
		acc = return_val[1]
		if (acc > best_acc):
			best_acc = acc
			best_feat_set = list(feature_set) 
	print("Finished search!! The best feature subset is {", end=' ')
	print(','.join(str(i) for i in best_feat_set), end=' ')
	print("}, which has an accuracy of ",best_acc,"%")

def backward(fileName):
	data_set = mkDataSet(fileName)
	instances = len(data_set)
	features = len(data_set[0]) - 1
	print("\nThis dataset has ",features," features (not including the class attribute), with "\
	,instances," instances.\n")
	# print("Normalizing data...", end=' ')
	# call normalize
	data_set = normalize(data_set)
	# print("Done!")
	flags = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	# call get_accuracy
	acc = get_accuracy(data_set, flags)
	print("Running nearest neighbor with all "\
	 ,features," features, using \"leaving-one-out\" evaluation, I get an accuracy of "\
	 ,acc,"%\n")
	print("Beginning search.\n")
	pos_flags = [i for i in range(1, features + 1)]
	feature_set = [i for i in range(1, features + 1)]
	best_feat_set = [i for i in range(1, features + 1)]
	best_acc = 0.0
	for i in range(features - 1):
		return_val = get_backward_feature_set(data_set, pos_flags, feature_set, best_acc)
		feature_set = return_val[0]
		acc = return_val[1]
		if (acc > best_acc):
			best_acc = acc
			best_feat_set = list(feature_set) 
	print("Finished search!! The best feature subset is {", end=' ')
	print(','.join(str(i) for i in best_feat_set), end=' ')
	print("}, which has an accuracy of ",best_acc,"%")

def special(fileName):
	data_set = mkDataSet(fileName)
	instances = len(data_set)
	features = len(data_set[0]) - 1
	print("\nThis dataset has ",features," features (not including the class attribute), with "\
	,instances," instances.\n")
	# print("Normalizing data...", end=' ')
	# call normalize
	data_set = normalize(data_set)
	# print("Done!")
	flags = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	acc = get_accuracy(data_set, flags)
	print("Running nearest neighbor with all "\
	 ,features," features, using \"leaving-one-out\" evaluation, I get an accuracy of "\
	 ,acc,"%\n")
	print("Beginning search.\n")
	pos_flags = [i for i in range(1, features + 1)]
	feature_set = []
	best_feat_set = []
	best_acc = 0.0
	# feature evaluation for single features
	acc = 0.0
	current_features = []
	flags_left = [i for i in pos_flags if i not in current_features]
	flag_scores = [0.0] * len(flags_left)
	current_index = 0
	for i in flags_left:
		flags = [0] * (len(pos_flags) + 1)
		flags[i] = 1
		for j in current_features:
			flags[j] = 1
		acc = get_accuracy(data_set, flags)
		flag_scores[current_index] = acc
		feature_set = list(current_features)
		feature_set.append(i)
		print("Using feature(s) {", end=' ')
		if (len(feature_set) == 1):
			print(feature_set[0], end=' ')
		else:
			print(','.join(str(i) for i in feature_set), end=' ')
		print("} accuracy is ",flag_scores[current_index],"%")
		current_index = current_index + 1
	feature_set = list(current_features)
	y = max(flag_scores)
	for i in range(len(flags_left)):
		if (flag_scores[i] == y):
			feature_set.append(flags_left[i])
			break
	sorted_scores = [(0.00, 0)] * (len(flag_scores))
	for i in range(len(flag_scores)):
		sorted_scores[i] = (flag_scores[i], i + 1)
	sorted_scores = sorted(sorted_scores)
	print("\nFeature set{", end=' ')
	if (len(feature_set)== 1):
		print(feature_set[0], end=' ')
	else:
		print(','.join(str(i) for i in feature_set), end=' ')
	print("} was best, accuracy is ", y,"%\n")
	acc = y
	if (acc > best_acc):
		best_acc = acc
		best_feat_set = list(feature_set) 
	return_val = get_special_feature_set(data_set, sorted_scores, best_acc)
	best_feat_set = return_val[0]
	best_acc = return_val[1]
	print("Finished search!! The best feature subset is {", end=' ')
	print(','.join(str(i) for i in best_feat_set), end=' ')
	print("}, which has an accuracy of ",best_acc,"%")

# main menu
fileName = ""
choice = 0
print("Welcome to the Feature Selection Algorithm!")
while(1):	
	try:
		fileName = input('Type in the name of the file to test: ')
		open(fileName)
	except EnvironmentError :
		print("Error: Cannot find ",fileName,".")
		continue
	else:
		break
print("\nType in the number of the algorithm you want to test: ")
print("1) Forward Selection")
print("2) Backward Elimination")
print("3) Special Algorithm")
choice = eval(input())
if (choice == 1):
	forward(fileName)
elif (choice == 2):
	backward(fileName)
elif (choice == 3):
	special(fileName)	