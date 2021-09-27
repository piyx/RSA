from collections import Counter, defaultdict
import heapq
import json
import os


class HeapNode:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq
    
    def __gt__(self, other):
        return self.freq > other.freq
    
    def __eq__(self, other):
        return self.freq = other.freq


def chunks(sequence, chunksize):
    n = len(sequence)
    for i in range(0, n, chunksize):
        yield sequence[i:i+chunksize]



class HuffmanCoding:
    def __init__(self):
        pass
    
    
    def generate_tree(self, heap: list[HeapNode]) -> HeapNode:
        heapq.heapify(heap)

        while len(heap) > 1:
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)
            heapq.heappush(
                heap, 
                HeapNode(
                    char='', 
                    freq=node1.freq+node2.freq,
                    left=node1,
                    right=node2
                )
            )

        return heapq.heappop(heap)
    
    
    def generate_encoding_map(self, filename: str) -> None:
        with open(filename, 'r') as f:
            heap = [HeapNode(char=char, freq=freq) for char, freq in Counter(f.read()).items()]
        
        encodingmap = defaultdict(str)

        def generate_encoding(node: HeapNode, encoding: str) -> None:
            if not node: return
            encodingmap[node.char] = encoding
            generate_encoding(node.left, encoding+'0')
            generate_encoding(node.right, encoding+'1')

        root = self.generate_tree(heap)
        generate_encoding(root, '')
        del encodingmap['']
        return encodingmap


    def encodetext(self, text: str, encodingmap: dict[str, str]) -> str:
        return ''.join(encodingmap[char] for char in text)


    def addpadding(self, encodedtext: str) -> str:
        padlen = 8 - (len(encodedtext) % 8)
        padinfo = f"{padlen:08b}"
        return ''.join([padinfo, encodedtext, '0'*padlen])


    def removepadding(self, encodedtext: str) -> str:
        padinfo = encodedtext[:8]
        padlen = int(padinfo, 2)
        return encodedtext[8:-1*padlen]
    

    def decodetext(self, text: str, decodingmap: dict[str, str]) -> str:
        decodedchars = []
        curr = ""

        for bit in text:
            curr += bit
            if curr in decodingmap:
                char = decodingmap[curr]
                decodedchars.append(char)
                curr = ""
        
        return ''.join(decodedchars)
    

    def compress(self, filename: str) -> None:
        encodingmap = self.generate_encoding_map(filename)
        outputfile = os.path.splitext(filename)[0] + '.bin'
        
        with open(filename, 'r+') as f:
            encodedtext = self.encodetext(f.read(), encodingmap)
            encodedtext = self.addpadding(encodedtext)

        with open(outputfile, 'wb') as f:
            f.write(bytes(bytearray([int(chunk, 2) for chunk in chunks(encodedtext, 8)])))
        
        with open("encoding.json", 'w') as f:
            json.dump(encodingmap, f)
    

    def decompress(self, filename: str, encodingfile: str) -> None:
        with open(encodingfile, 'r') as f:
            encodingmap = json.load(f)
        
        outputfile = os.path.splitext(filename)[0] + '_decompressed' + '.txt'
        decodingmap = {encoding: char for char, encoding in encodingmap.items()}
        
        with open(filename, 'rb') as f:
            text = "".join(bin(byte)[2:].rjust(8, '0') for byte in f.read())
            encodedtext = self.removepadding(text)
            decodedtext = self.decodetext(encodedtext, decodingmap)

        with open(outputfile, 'w') as f:
            f.write(decodedtext)


def main():
    huffman = HuffmanCoding()
    huffman.compress("test.txt")
    huffman.decompress("test.bin", "encoding.json")


if __name__=="__main__":
    main()
