import numpy as np

class Cube:
    # 0 - white (U)
    # 1 - green (F)
    # 2 - red (R)
    # 3 - blue (B)
    # 4 - orange (L)
    # 5 - yellow (D)
    def __init__(self,n):
        self.n = n
        self.stickers = [
            np.full((n,n), i) for i in range(6)
        ]
        self.colors = {
            0: '\033[37m',
            1: '\033[32m',
            2: '\033[31m',
            3: '\033[34m',
            4: '\033[38;2;255;165;0m',
            5: '\033[33m'
        }

    def swapStickersU(self, arr, w):
            buffer = np.copy(self.stickers[arr[3]][:w])
            self.stickers[arr[3]][:w] = np.copy(self.stickers[arr[0]][:w])
            self.stickers[arr[0]][:w] = np.copy(self.stickers[arr[1]][:w])
            self.stickers[arr[1]][:w] = np.copy(self.stickers[arr[2]][:w])
            self.stickers[arr[2]][:w] = np.copy(buffer)

    def swapStickersR(self, arr, w, order):
        if order == 1:
            buffer = np.copy(self.stickers[arr[3]][:, 0:w])[::-1, ::-1]
            self.stickers[arr[3]][:, 0:w:] = np.copy(self.stickers[arr[0]][:, self.n-w:])[::-1, ::-1]
            self.stickers[arr[0]][:, self.n-w:] = np.copy(self.stickers[arr[1]][:, self.n-w:])
            self.stickers[arr[1]][:, self.n-w:] = np.copy(self.stickers[arr[2]][:, self.n-w:])
            self.stickers[arr[2]][:, self.n-w:] = np.copy(buffer)
        elif order == -1 or order == 2:
            buffer = np.copy(self.stickers[arr[3]][:, 0:w][::-1, ::-1])
            self.stickers[arr[3]][:, 0:w] = np.copy(self.stickers[arr[2]][:, self.n-w:])[::-1, ::-1]
            self.stickers[arr[2]][:, self.n-w:] = np.copy(self.stickers[arr[1]][:, self.n-w:])
            self.stickers[arr[1]][:, self.n-w:] = np.copy(self.stickers[arr[0]][:, self.n-w:])
            self.stickers[arr[0]][:, self.n-w:] = np.copy(buffer)
    
    def swapStickersF(self, arr, w, order):
        if order == 1:
            buffer = np.copy(self.stickers[arr[3]][:, self.n-w:])
            self.stickers[arr[3]][:, self.n-w:] = np.copy(self.stickers[arr[2]][0:w, :].T[:, ::-1])
            self.stickers[arr[2]][0:w, :] = np.copy(self.stickers[arr[1]][:, 0:w].T[:, ::-1])
            self.stickers[arr[1]][:, 0:w] = np.copy(self.stickers[arr[0]][self.n-w:, :].T[:, ::-1])
            self.stickers[arr[0]][self.n-w:, :] = np.copy(buffer.T[:, ::-1])
        elif order == -1 or order == 2:
            buffer = np.copy(self.stickers[arr[3]][:, self.n-w:])
            self.stickers[arr[3]][:, self.n-w:] = np.copy(self.stickers[arr[0]][self.n-w:, :].T[::-1, :])
            self.stickers[arr[0]][self.n-w:, :] = np.copy(self.stickers[arr[1]][:, 0:w].T[::-1, :])
            self.stickers[arr[1]][:, 0:w] = np.copy(self.stickers[arr[2]][0:w, :].T[::-1, :])
            self.stickers[arr[2]][0:w, :] = np.copy(buffer.T[::-1, :])
        

    def U(self,w=1,order=1):
        self.stickers[0] = np.flip(self.stickers[0].T, axis=(1 if order==1 else 0))
        self.swapStickersU(arr=[1,2,3,4] if order == 1 else [4,3,2,1], w=w)   
        if order == 2:
            self.U(w, order=-1)
        # if rotating the cube we need to handle bottom face
        if w==self.n:
            self.stickers[5] = np.flip(self.stickers[5].T, axis=(0 if order==1 else 1))

    def D(self, w=1, order=1):
        #self.stickers[5] = np.flip(self.stickers[5].T, axis=(1 if order==1 else 0))
        self.U(w=self.n-w,order=order)
        self.U(w=self.n,order=order*-1 if order != 2 else 2)

    def R(self, w=1, order=1):
        self.stickers[2] = np.flip(self.stickers[2].T, axis=(1 if order==1 else 0))
        self.swapStickersR(arr=[0,1,5,3], w=w, order=order)   
        if order == 2:
            self.R(w, order=-1)
        # if rotating the cube we need to handle left face
        if w==self.n:
            self.stickers[4] = np.flip(self.stickers[4].T, axis=(0 if order==1 else 1))

    def L(self, w=1, order=1):
        #self.stickers[4] = np.flip(self.stickers[4].T, axis=(1 if order==1 else 0))
        self.R(w=self.n-w,order=order)
        self.R(w=self.n,order=order*-1 if order != 2 else 2)

    def F(self, w=1, order=1):
        self.stickers[1] = np.flip(self.stickers[1].T, axis=(1 if order==1 else 0))
        self.swapStickersF(arr=[0,2,5,4], w=w, order=order)   
        if order == 2:
            self.F(w, order=-1)
        # if rotating the cube we need to handle back face
        if w==self.n:
            self.stickers[3] = np.flip(self.stickers[3].T, axis=(0 if order==1 else 1))

    def B(self, w=1, order=1):
        #self.stickers[3] = np.flip(self.stickers[3].T, axis=(1 if order==1 else 0))
        self.F(w=self.n-w,order=order)
        self.F(w=self.n,order=order*-1 if order != 2 else 2)

    def scramble(self, scq, step_by_step = False):
        applied = ""
        for move in scq.split():
            ogmove = move
            width = 1
            # get the width of the move and remove the W
            if "w" in move:
                if move[0].isdigit():
                    width = int(move[0])
                    move = move[1:]
                else:
                    width = 2
                if move[-1] != 'w':
                    move = move[:-2] + move[-1]
                else:
                    move = move[:-1]
            #get the order
            order = 1
            # is prime? if so remove prime
            if move[-1] == "'":
                order = -1
                move = move[:-1]
            elif move[-1] == "2":
                order = 2
                move = move[:-1]

            if move == "R":
                self.R(width, order)
            elif move == "F":
                self.F(width,order)
            elif move == "U":
                self.U(width,order)
            elif move == "D":
                self.D(width, order)
            elif move == "L":
                self.L(width, order)
            elif move == "B":
                self.B(width, order)
            
            if step_by_step:
                print(f"Applied:{applied} {self.colors[1]}{ogmove}\033[0m\n")
                print(self)
                applied+=f" {ogmove}"
    




    def __str__(self):
        #outstr = "-------------------\n\n"
        outstr = "\n"

        #print U
        for i in range(self.n):
            outstr += "  "*self.n+"   "
            for j in range(self.n):
                sticker = self.stickers[0][i][j]
                outstr+=f'{self.colors[sticker]}{str(sticker)} '
            outstr+="\n"
        outstr+="\n"
        # print lfrb
        for i in range(self.n):
            for face in [4,1,2,3]:
                for j in range(self.n):
                    sticker = self.stickers[face][i][j]
                    outstr+=f'{self.colors[sticker]}{str(sticker)} '
                outstr+="   "
            outstr+="\n"
        outstr+="\n"
        #print d
        for i in range(self.n):
            outstr += "  "*self.n+"   "
            for j in range(self.n):
                sticker = self.stickers[5][i][j]
                outstr+=f'{self.colors[sticker]}{str(sticker)} '
            outstr+="\n"
        outstr+="\033[0m\n-------------------"
        
        return outstr

    
if __name__ == "__main__":
    c = Cube(7)
    print(c)
    c.scramble("3Uw D Bw Fw' Uw Lw' Bw L2 D' B' 3Fw Uw' U' F B R' Dw2 Fw L R' B L2 R' Lw2 B2 3Lw' U F Rw2 3Uw2 Rw R Dw2 D Rw' 3Bw 3Lw B 3Rw Bw2 Lw' 3Rw' L' 3Dw' Fw2 3Lw' Uw2 Fw' 3Bw 3Dw2 L Fw 3Fw Rw2 U 3Rw 3Bw Lw2 3Fw2 3Dw' 3Lw2 B2 3Uw Uw 3Fw2 Rw2 D 3Uw2 L2 3Lw2 F' Rw2 Dw Fw' 3Fw' Bw' D 3Bw' Uw' 3Fw2 Dw' Uw D' 3Uw2 3Dw' 3Fw2 Dw2 Fw' Uw2 L D2 3Fw D' R 3Fw Lw2 3Lw 3Bw2 U Rw'")
    print(c)
    #c.scramble("F 3Rw",step_by_step=True)