#!/usr/bin/python3
"""AEUsb - Скрипт для ассиметричного шифрования через ключ на флеш-накопителе
Copyright (c) 2023 Okulus Dev
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
import os
import sys
from psutil import disk_partitions
from colorama import init, Fore, Style
from cryptography.fernet import Fernet

RED = Fore.RED
LRED = Fore.LIGHTRED_EX
GREEN = Fore.GREEN
LGREEN = Fore.LIGHTGREEN_EX
YELLOW = Fore.YELLOW
LYELLOW = Fore.LIGHTYELLOW_EX
BLUE = Fore.BLUE
LBLUE = Fore.LIGHTBLUE_EX
END = Style.RESET_ALL


def check_key(filename: str) -> str:
	for disk in disk_partitions():
		if os.path.isfile(os.path.join(disk[1], filename)):
			return str(os.path.join(disk[1], filename))

	print(f'{RED}[!] Подключите флешку с ключом!{END}')
	return None


def write_key():
	print(f'{LBLUE}[+] Генерация ключа...{END}')
	key = Fernet.generate_key()
	
	with open('aeusb.key', 'wb') as key_file:
		key_file.write(key)
	
	print(f'{LBLUE}[+] Ключ сохранен в aeusb.key. Сохраните его на флешку{END}')


def load_key():
	keypath = check_key('aeusb.key')

	if keypath is None:
		write_key('aeusb.key')
		keypath = check_key('aeusb.key')

		return open(keypath, 'rb').read()
	else:
		return open(keypath, 'rb').read()


def encrypt_file(filename):
	key = load_key()
	f = Fernet(key)
	
	with open(filename, 'rb') as file:
		file_data = file.read()
	
	encrypted_data = f.encrypt(file_data)
	print(f'{GREEN}[+] {filename} зашифрован{END}')
	
	with open(filename, 'wb') as file:
		file.write(encrypted_data)


def encrypt_directory(crypt_dir: str):
	try:
		for file in os.listdir(crypt_dir):
			if os.path.isdir(f'{crypt_dir}/{file}'):
				encrypt_directory(f'{crypt_dir}/{file}')
			if os.path.isfile(f'{crypt_dir}/{file}'):
				try:
					encrypt_file(f'{crypt_dir}/{file}')
				except Exception as e:
					pass
	except Exception as e:
		print(e)


def decrypt_file(filename):
	key = load_key()
	f = Fernet(key)
	
	with open(filename, 'rb') as file:
		encrypted_data = file.read()
	
	decrypted_data = f.decrypt(encrypted_data)
	print(f'{GREEN}[+] Файл {filename} расшифрован{END}')
	
	with open(filename, 'wb') as file:
		file.write(decrypted_data)


def decrypt_directory(decrypt_dir):
	try:
		for file in os.listdir(decrypt_dir):
			if os.path.isdir(f'{decrypt_dir}/{file}'):
				decrypt_directory(f'{decrypt_dir}/{file}')
			if os.path.isfile(f'{decrypt_dir}/{file}'):
				try:
					decrypt_file(f'{decrypt_dir}/{file}')
				except Exception as e:
					pass
	except Exception as e:
		print(e)


def main():
	key_exists = False

	for disk in disk_partitions():
		if os.path.isfile(os.path.join(disk[1], 'aeusb.key')):
			print(f'{GREEN}[+] Ключ найден: {os.path.join(disk[1], "aeusb.key")}{END}')
			key_exists = True
			break

	if key_exists == False:
		print(f'{YELLOW}[!] Внимание! Ключ не найден! Используйте genkey{END}')
		return

	try:
		cord = sys.argv[1]
		
		if cord == 'crypt':
			try:
				encrypt_directory(sys.argv[2])
			except Exception as e:
				print(e)
		elif cord == 'decrypt':
			try:
				decrypt_directory(sys.argv[2])
			except Exception as e:
				print(e)
		elif cord == 'genkey':
			write_key()
		else:
			print(f'\n{LRED}[!] Неправильная команда. Используйте: genkey; crypt <директория>; decrypt <директория>{END}')
	except IndexError:
		print(f'\n{LRED}[!] Вы не ввели аргументы. Используйте: genkey; crypt <директория>; decrypt <директория>{END}')


if __name__ == '__main__':
	main()
