import os
import Process


if __name__ == '__main__':
    # read file
    file_name_list = os.listdir('./pic')
    print(file_name_list)
    for file_name in file_name_list:
        result = Process.process_img(f'./pic/{file_name}')

        with open(f'output/{file_name.split(".")[0]}.txt', 'w', encoding='utf-8') as file:
            file.write(result)
        print(f'{file_name}: ')
        print(result)
