
import os
import sys
from datetime import date
import random
import shutil

'''
a.	Identifies 5% of distinct customer IDs and creates a NEW text file in same folder with ONLY decrypted customer IDs (will never be more than 100k rows)
b.	Creates additional text files for remaining 95% (target) with only APIDs up to 100K rows
c.	Creates additional text files for rows 100,001 - 200,000 then 200,001 - 300,000 etc.
'''

wild_card_date = str(date.today())
base_directory =  os.path.dirname(os.path.realpath(__file__))





def make_folder(folder_name):

	try: 
	    os.makedirs(folder_name[:-4] +'_' + wild_card_date)
	    return folder_name[:-4] +'_' + wild_card_date
	except OSError:
	    if not os.path.isdir(folder_name +'_' + wild_card_date):
	        raise


 
def read_file(file_name):

	all_customer_list = []
	with open(file_name) as f:
		for line in f:
			all_customer_list.append(line) # a list of all the rows on the text file
	print('>>>input file has ' + str(len(all_customer_list)) + ' rows')
	return all_customer_list

def get_unique_customers(all_customer_list):

	unique_customers = set([row.strip().split('\t')[1]  for row in all_customer_list])
	print('>>>' + str(len(unique_customers)) + ' unique customer_ids')
	return unique_customers



def get_sample(unique_customers):

	sample_size = int(len(unique_customers) * 0.05)
	random_sample_customer = random.sample(unique_customers, sample_size) # creates a list of randon customer_ids
	print('>>>sample size is ' + str(sample_size) + ' customers')
	return random_sample_customer



def write_out_sample_file(random_sample_customer, input_folder_path, file_name):

	with open(os.path.join(input_folder_path, '5%_' + file_name) , 'w') as f:
		for customer in random_sample_customer:
			f.write(customer + '\n') # creates the file with the 5% sample of customer_ids



def get_APIDs_for_not_in_sample_customers(all_customer_list, customer_ids_to_exclude):

	output_list_of_apids = [] # list of lists of APIDs. each list will be less than 100K
	one_k = [] # list of APIDs
	counter = 0
	unique_apids_set = set([row.strip().split('\t')[0] for row in all_customer_list if row.strip().split('\t')[1] not in customer_ids_to_exclude ]) # removes duplicate AIPDs

	for apid in unique_apids_set:
		
		if counter < 99999:
			one_k.append(apid)
			counter = counter + 1
		else:
			output_list_of_apids.append(one_k)
			one_k = []
			one_k.append(apid)
			counter = 0 

	output_list_of_apids.append(one_k)
	print('>>>target group contains ' + str(len(unique_apids_set)) + ' unique APIDs')
	print('>>>target segment was split into ' + str(len(output_list_of_apids)) + ' text file(s)')
	return output_list_of_apids


def write_out_AIPDs_text_files(output_list, input_folder_path, file_name):

	files = 1
	for l in output_list:
		with open(os.path.join(input_folder_path, 'output_{0}_'.format(files) + file_name ) , 'w') as f:
			for customer in l:
				f.write(customer + '\n')
		files = files + 1
	print('>>>data is ready')


def move_main_file_to_created_folder(input_folder_path, file_name):
	
	shutil.move(file_name, input_folder_path)



def main():

	file_name = sys.argv[1]
	folder = make_folder(file_name)
	input_folder_path = os.path.join(base_directory, folder)
	all_customer_list = read_file(file_name)
	unique_customers = get_unique_customers(all_customer_list)
	random_sample_customer = get_sample(unique_customers)
	write_out_sample_file(random_sample_customer, input_folder_path, file_name)
	write_out_AIPDs_text_files(get_APIDs_for_not_in_sample_customers(all_customer_list, random_sample_customer), input_folder_path, file_name)
	move_main_file_to_created_folder(input_folder_path, file_name)
	
	
	
	
	
	
main()
