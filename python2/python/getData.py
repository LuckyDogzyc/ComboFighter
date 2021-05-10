import json
import matplotlib.pyplot as plt

if __name__ == '__main__':
    with open('testCombos.json', 'r') as file:
        data = json.load(file)
    
    x = []
    y = []
    
    for i in data['top']:
        x.append(i)
        y.append(data['top'].get(i)[0][0])
    
    plt.plot(x, y)
    
    plt.xlabel('Rounds')
    plt.ylabel('Fitness')
    
    plt.title('Combo Fitness Over Time')
    
    plt.show()