import hashlib

def solution():
    print (
        '''Glückwunsch zum Lösen der 24 Rätsel. Um den finalen 6-stelligen Code zu erhalten, musst du die Funktion decode() mit der korrekt ausgefüllten Library unten aufrufen. Für jeden Tag musst du dabei die richtige zweistellige Zahl eingeben.
        
        solution_dictionary = {
        "1": "",
        "2": "",
        "3": "",
        "4": "",
        "5": "",
        "6": "",
        "7": "",
        "8": "",
        "9": "",
        "10": "",
        "11": "",
        "12": "",
        "13": "",
        "14": "",
        "15": "",
        "16": "",
        "17": "",
        "18": "",
        "19": "",
        "20": "",
        "21": "",
        "22": "",
        "23": ""
    }
        '''
    )
    return

solution_list = ['1a6562590ef19d1045d06c4055742d38288e9e6dcd71ccde5cee80f1d5a774eb', 'e629fa6598d732768f7c726b4b621285f9c3b85303900aa912017db7617d8bdb', '4ec9599fc203d176a301536c2e091a19bc852759b255bd6818810a42c5fed14a', 'c2356069e9d1e79ca924378153cfbbfb4d4416b1f99d41a2940bfdb66c5319db', '8c1f1046219ddd216a023f792356ddf127fce372a72ec9b4cdac989ee5b0b455', '6b51d431df5d7f141cbececcf79edf3dd861c3b4069f0b11661a3eefacbba918', '785f3ec7eb32f30b90cd0fcf3657d388b5ff4297f2f9716ff66e9b69c05ddd09', 'da4ea2a5506f2693eae190d9360a1f31793c98a1adade51d93533a6f520ace1c', '6cd5b6e51936a442b973660c21553dd22bd72ddc8751132a943475288113b4c0', '6b51d431df5d7f141cbececcf79edf3dd861c3b4069f0b11661a3eefacbba918', 'b17ef6d19c7a5b1ee83b907c595526dcb1eb06db8227d650d5dda0a9f4ce8cd9', 'f369cb89fc627e668987007d121ed1eacdc01db9e28f8bb26f358b7d8c4f08ac', '349c41201b62db851192665c504b350ff98c6b45fb62a8a2161f78b6534d8de9', 'a21855da08cb102d1d217c53dc5824a3a795c1c1a44e971bf01ab9da3a2acbbf', 'b4944c6ff08dc6f43da2e9c824669b7d927dd1fa976fadc7b456881f51bf5ccc', '0b8efa5a3bf104413a725c6ff0459a6be12b1fd33314cbb138745baf39504ae5', '44c8031cb036a7350d8b9b8603af662a4b9cdbd2f96e8d5de5af435c9c35da69', '535fa30d7e25dd8a49f1536779734ec8286108d115da5045d77f3b4185d8f790', 'aacd834b5cdc64a329e27649143406dd068306542988dfc250d6184745894849', 'e29c9c180c6279b0b02abd6a1801c7c04082cf486ec027aa13515e4f3884bb6b', '8527a891e224136950ff32ca212b45bc93f69fbb801c3b1ebedac52775f99e61', '8527a891e224136950ff32ca212b45bc93f69fbb801c3b1ebedac52775f99e61', '9400f1b21cb527d7fa3d3eabba93557a18ebe7a2ca4e471cfe5e4c5b4ca7f767']
solution_sentence_list = [68, 117, 32, 104, 97, 115, 116, 32, 97, 108, 108, 101, 32, 82, 228, 116, 115, 101, 108, 32, 101, 114, 102, 111, 108, 103, 114, 101, 105, 99, 104, 32, 103, 101, 108, 246, 115, 116, 46, 32, 68, 97, 115, 32, 76, 246, 115, 117, 110, 103, 115, 119, 111, 114, 116, 32, 105, 115, 116, 32, 101, 105, 110, 32, 70, 97, 114, 98, 116, 111, 110, 46, 32, 72, 228, 116, 116, 101, 32, 69, 108, 109, 111, 115, 32, 70, 101, 108, 108, 32, 110, 105, 99, 104, 116, 32, 100, 105, 101, 115, 101, 110, 32, 70, 97, 114, 98, 116, 111, 110, 44, 32, 107, 246, 110, 110, 116, 101, 32, 101, 114, 32, 100, 105, 99, 104, 32, 110, 105, 99, 104, 116, 32, 97, 108, 115, 32, 84, 97, 114, 110, 117, 110, 103, 32, 117, 110, 116, 101, 114, 115, 116, 252, 116, 122, 101, 110, 46]

def sentence_decode():
    decoded_solution_list = []
    for i in solution_sentence_list:
        decoded_solution_list.append(chr(i))
    print("".join(decoded_solution_list))
    return decoded_solution_list

def decode(solution_dictionary):
    result_dictionary = {}
    for i in range(23):
        correct_solution = solution_list[i]
        provided_solution = hashlib.sha256(bytes(solution_dictionary[str(i+1)], "utf-8")).hexdigest()
        result_dictionary[str(i+1)] = correct_solution == provided_solution
    t = 0
    c = 0
    for i in range(23):
        if result_dictionary[str(i+1)] == True:
            t = t+1
            c = c+1
            print(str(t) + " = True")
        else:
            t = t+1
            print(str(t) + " = False")
    if c == 23:
        sentence_decode()
        return solution_dictionary
    elif c != 23:
        print("Starte einen neuen Versuch.")
        return solution_dictionary