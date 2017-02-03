import csv, os, operator

n_runs = 3
frequencies = [100, 200, 300]
n_nodes = [2, 4, 8, 16, 32, 64, 128, 256]
aggregate_dir = "aggregated_data"

def aggregateRawCsvFiles(list_of_file_names, aggregateFileName):
	# data = {0:{"total":2, "count":3}, 1:{"total":6, "count":3}}
	data = {}
	for filename in list_of_file_names:
		with open(filename) as inputCSV:
			reader = csv.DictReader(inputCSV, fieldnames=["id", "sent_ns", "recv_ns"])

			for row in reader:
				if row["sent_ns"] is None or row["recv_ns"] is None:
					continue
				
				row_id = int(row["id"])
				row_sent_ns = long(row["sent_ns"])
				row_recv_ns = long(row["recv_ns"])


				if not row_id in data:
					data[row_id] = {"total":0, "count":0}

				data[row_id]["total"] += (row_recv_ns - row_sent_ns) / 1000000.0
				data[row_id]["count"] += 1

	with open(aggregateFileName, "w+") as outputCSV:
		fieldnames = ["id", "Mean Message Latency (ms)"]
		writer = csv.DictWriter(outputCSV, fieldnames=fieldnames)
		writer.writeheader()

		for message_id, values in sorted(data.items(), key=operator.itemgetter(0)):
			row_data = {"id":message_id}
			row_data["Mean Message Latency (ms)"] = values["total"] / float(values["count"])

			writer.writerow(row_data)

def collectRunsAndNodesTogether():
	for freq in frequencies:
		for total_nodes in n_nodes:
			# Aggregates across all individual nodes and runs
			filenames = []
			for current_node in range(total_nodes / 2):
				for run in range(1, n_runs+1):
					fname = "times_{}Hz_{}nodes_{}node.csv".format(freq, total_nodes, current_node)
					path = os.path.join("run_"+str(run), fname)

					filenames.append(path)
					print(path)

			# perform aggregation
			print("Aggregating")
			aggregateRawCsvFiles(filenames, "{}/agg_times_{}Hz_{}nodes.csv".format(aggregate_dir, freq, total_nodes))

def aggregateFrequencyCsvFiles(list_of_file_names, list_of_total_node_counts, aggregateFileName):
	# data = {0:{"2":{"total":2, "count":3},"4": {"total":2, "count":3}, 
	#        1:{"2":{"total":4, "count":32},"4": {"total":4, "count":4}}}
	data = {}
	for filename, total_node_count in zip(list_of_file_names, list_of_total_node_counts):
		with open(filename) as inputCSV:
			reader = csv.DictReader(inputCSV, fieldnames=["id", "Mean Message Latency (ms)"])
			next(reader, None)  # skip the headers

			for row in reader:
				row_id = int(row["id"])
				row_msg_lat_ms = float(row["Mean Message Latency (ms)"])

				if not row_id in data:
					data[row_id] = {}

				if not total_node_count in data[row_id]:
					data[row_id][total_node_count] = {"total":0, "count":0}

				data[row_id][total_node_count]["total"] += row_msg_lat_ms
				data[row_id][total_node_count]["count"] += 1

	with open(aggregateFileName, "w+") as outputCSV:
		fieldnames = ["id"]
		for total_node_count in list_of_total_node_counts:
			fieldnames.append("{} Nodes".format(total_node_count))
		writer = csv.DictWriter(outputCSV, fieldnames=fieldnames)
		writer.writeheader()

		
		for message_id, values in sorted(data.items(), key=operator.itemgetter(0)):
			row_data = {"id":message_id}

			for total_node_count, total_obj in values.items():
				row_data["{} Nodes".format(total_node_count)] = total_obj["total"] / float(total_obj["count"])

			writer.writerow(row_data)

def collectTotalNodesTogether():
	for freq in frequencies:
		filenames = []
		node_counts = []
		for total_nodes in n_nodes:
			fname = "agg_times_{}Hz_{}nodes.csv".format(freq, total_nodes)
			path = os.path.join(aggregate_dir, fname)

			filenames.append(path)
			node_counts.append(total_nodes)
			print(path)

		# perform aggregation
		print("Aggregating")
		aggregateFrequencyCsvFiles(filenames, node_counts, "agg_times_{}Hz.csv".format(freq))

def main():
	collectRunsAndNodesTogether()
	collectTotalNodesTogether()
			

if __name__ == "__main__":
    main()
