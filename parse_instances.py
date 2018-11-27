import re
import sys

instance_length = int(sys.argv[1])
instance_index = 0
instance_count = 0

file = None

for line in sys.stdin:
    if len(line.strip()) == 0: 
        continue

    
    if instance_count <= 0:
        instance_index = instance_index + 1
        instance_count = instance_length * 3
        
        if file != None:
            file.close()

        file = open('instances/wt' + str(instance_length) + '_i' + str(instance_index) + '.txt', 'w')
    
    line_of_ints = re.sub('[\s\n]+', ':', line.strip())

    for number in line_of_ints.split(':'):
        instance_count = instance_count - 1
        file.write(number)
        file.write('\n')
        
        