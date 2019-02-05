from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import logging
import os
from os import path
import json
# from t_t import engine
import glob


app = Flask(__name__)



def engine(data):
    #try:

        
        import cv2 as cv
        import numpy as np
        from collections import Counter
        from statistics import mean

        acne_string = []
        trust_score = []

        
        


        image = cv.imdecode(np.fromstring(data, np.uint8), cv.IMREAD_UNCHANGED)

        
        

        u = image
        
        # to remove noise first we use smoothing technique
        smoothing = cv.GaussianBlur(u, (5, 5), cv.BORDER_DEFAULT)


        # lets convert this to gray scale

        img_grey = cv.cvtColor(smoothing.copy(), cv.COLOR_BGR2GRAY)

        th = cv.adaptiveThreshold(img_grey.copy(), 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 147,
                                  4)  # 37

        kernel3 = np.ones((7, 7), np.uint8)

        opening = cv.morphologyEx(th.copy(), cv.MORPH_OPEN, kernel3)

        (im2, contours, hierarchy) = cv.findContours(opening.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        #marked_image = cv.drawContours(u.copy(), contours, -1, (0, 0, 255), 1)
        '''
        plt.imshow(cv.cvtColor(marked_image,cv.COLOR_BGR2RGB))
        plt.axis("off")
        plt.show()
        '''
        # threshold_area = 5000
        spotcontour = []
        spotarea = []
        combined = {}
        for cnt in contours:
            area = cv.contourArea(cnt)
            spotcontour.append(cnt)
            spotarea.append(area)

        p = 0
        for a in spotarea:
            combined[a] = spotcontour[p]
            p += 1

        # len(spotarea)
        # len(spotcontour)
        # len(combined)

        intensity = []

        # For each list of contour points...
        for i in range(len(spotcontour)):
            # Create a mask image that contains the contour filled in
            cimg = np.zeros_like(u.copy())
            cv.drawContours(cimg, spotcontour, i, color=255, thickness=-1)

            # Access the image pixels and create a 1D numpy array then add to list
            pts = np.where(cimg == 255)
            intensity.append(u[pts[0], pts[1]])
        B = []
        G = []
        R = []
        b = []
        g = []
        r = []
        k = []
        i = 0
        for l in range(0, len(intensity)):
            for m in intensity[l]:
                for j in m:
                    k.append(j)
                B.append(k[i])
                G.append(k[i + 1])
                R.append(k[i + 2])
                i = i + 3
            b.append(mean(B))
            g.append(mean(G))
            r.append(mean(R))

        fin = []

        for i in range(0, len(spotarea)):

            if ((spotarea[i] <= 75) and ((r[i] >= 160 and r[i] <= 230) and (g[i] >= 100 and g[i] <= 185) and (
                    b[i] >= 50 and b[i] <= 180))):
                fin.append("SP")

            elif ((spotarea[i] >= 75 and spotarea[i] <= 500) and (
                    (r[i] >= 120 and r[i] <= 216) and (g[i] >= 40 and g[i] <= 160) and (
                    b[i] >= 20 and b[i] <= 180))):

                fin.append("MP")

            elif ((spotarea[i] >= 500 and spotarea[i] <= 8000) and (r[i] >= 50 and r[i] <= 230) and (
                    g[i] >= 30 and g[i] <= 140) and (b[i] >= 20 and b[i] <= 150)):
                fin.append("LP")

            elif ((r[i] >= 0 and r[i] <= 90) and (g[i] >= 0 and g[i] <= 90) and (b[i] >= 0 and b[i] <= 90)):
                fin.append("A")
            else:

                fin.append("UNK")

        ff = Counter(fin)

        perc = {}
        for i, j in ff.items():
            cev = (j / len(spotarea) * 100)
            perc[i] = cev

        def pgmil():
            gk = []
            if spotarea >= 100 and spotarea <= 360:
                gk.append(35)
            else:
                gk.append(0)
            if SP >= 4 and SP <= 60:
                gk.append(15)
            else:
                gk.append(0)
            if unk >= 0 and unk <= 70:
                gk.append(10)
            else:
                gk.append(0)
            if MP >= 0 and MP <= 65:
                gk.append(10)
            else:
                gk.append(0)
            if LP >= 0 and LP <= 12:
                gk.append(10)
            else:
                gk.append(0)
            if A == 0:
                gk.append(5)
            else:
                gk.append(0)
            if R >= 130 and R <= 240:
                gk.append(5)
            else:
                gk.append(0)
            if G >= 90 and G <= 170:
                gk.append(5)
            else:
                gk.append(0)
            if B >= 60 and B <= 145:
                gk.append(5)
            else:
                gk.append(0)
            mm = sum(gk)
            return mm

        def pgmed():
            gk = []
            if spotarea >= 100 and spotarea <= 1010:
                gk.append(35)
            else:
                gk.append(0)
            if SP >= 1 and SP <= 40:
                gk.append(15)
            else:
                gk.append(0)
            if unk >= 0 and unk <= 83.49:
                gk.append(10)
            else:
                gk.append(0)
            if MP >= 0 and MP <= 55:
                gk.append(10)
            else:
                gk.append(0)
            if LP >= 0 and LP <= 30:
                gk.append(10)
            else:
                gk.append(0)
            if A >= 0:
                gk.append(5)
            else:
                gk.append(0)
            if R >= 140 and R <= 230:
                gk.append(5)
            else:
                gk.append(0)
            if G >= 80 and G <= 160:
                gk.append(5)
            else:
                gk.append(0)
            if B >= 60 and B <= 150:
                gk.append(5)
            else:
                gk.append(0)
            mm = sum(gk)

            return mm

        def pgsv():
            gk = []
            if spotarea >= 350 and spotarea < 1100:
                gk.append(35)
            else:
                gk.append(0)
            if SP >= 0 and SP <= 35:
                gk.append(15)
            else:
                gk.append(0)
            if unk >= 0 and unk <= 35:
                gk.append(10)
            else:
                gk.append(0)
            if MP >= 2 and MP <= 55:
                gk.append(10)
            else:
                gk.append(0)
            if LP >= 15 and LP <= 40:
                gk.append(10)
            else:
                gk.append(0)
            if A > 0:
                gk.append(5)
            else:
                gk.append(0)
            if R >= 130 and R <= 200:
                gk.append(5)
            else:
                gk.append(0)
            if G >= 70 and G <= 155:
                gk.append(5)
            else:
                gk.append(0)
            if B >= 30 and B <= 160:
                gk.append(5)
            else:
                gk.append(0)


            mm = sum(gk)

            return mm

        spotarea = mean(spotarea)
        try:
            SP = perc['SP']
        except:
            SP = 0
        try:
            unk = perc['unk']
        except:
            unk = 0
        try:
            MP = perc['MP']
        except:
            MP = 0
        try:
            LP = perc['LP']
        except:
            LP = 0
        try:
            A = perc['A']
        except:
            A = 0
        # Classifying

        R = mean(r)
        G = mean(g)
        B = mean(b)
        kk = 0
        if ((spotarea >= 100 and spotarea <= 360) and (SP >= 4 and SP <= 60) and (unk >= 0 and unk <= 70) and (
                MP >= 0 and MP <= 65) and (LP >= 0 and LP <= 12) and (A == 0) and (R >= 130 and R <= 240) and (
                G >= 90 and G <= 170) and (B >= 60 and B <= 145)):
            kk = pgmil()

            # print('Mild Acne Detected \n')
            acne_string.append('Mild')
            trust_score.append(kk)
            # print('Trust Score of Mild Acne out of 100.. is',kk)



        elif ((spotarea >= 100 and spotarea <= 1010) and (SP >= 1 and SP <= 40) and (unk >= 0 and unk <= 84) and (
                MP >= 0 and MP <= 65) and (LP >= 0 and LP <= 30) and (A >= 0) and (R >= 140 and R <= 230) and (
                      G >= 80 and G <= 160) and (B >= 60 and B <= 150)):
            kk = pgmed()
            # print('Moderate level Acne Detected \n')
            acne_string.append('Moderate')
            trust_score.append(kk)
            # print('Trust Score of Moderate Acne out of 100.. is ',kk)


        elif ((spotarea >= 350 and spotarea <= 1100) and (SP >= 0 and SP <= 35) and (unk >= 0 and unk <= 35) and (
                MP >= 2 and MP <= 65) and (LP >= 15 and LP <= 40) and (A >= 0) and (R >= 130 and R <= 200) and (
                      G >= 70 and G <= 155) and (B >= 30 and B <= 160)):
            kk = pgsv()
            # print('Severe Acne Detected \n')
            acne_string.append('Severe')
            trust_score.append(kk)
            # print('Trust Score of Severe Acne out of 100.. is ',kk)


        else:

            acne_string.append('Not_identified')
            trust_score.append(0)

            


        return acne_string,trust_score


                # print('Please take the photo in the good lighting condition')
                # op='Please take the photo in the good lighting condition'

            # T=time.time() - start_time
            # print("--- %s seconds ---" % T)

            # if T >= 11:

            # op='Not able to recognize Acne'
            # jfk=0

        # for 4 images
        







    #except:

        #op = 'Could not recognize Acne'
        #jfk = 0
        #ex = 'exception occured'

        
@app.route("/upload", methods = ['GET','POST'])
#def hello():
    #return "Hello World!"
def Upload_image():
    #import cv2 as cv
    def avg(lst): 
        return sum(lst) / len(lst) 
    acne_string=[]
    trust_score=[]
    
    files=request.files["image1"]
    
    
    #img_data=files.read()
    if files:
        
        return "this sHit should work"
    else:
        return "this shit is not working"
'''
    ass, ts, = engine(img_data)
    acne_string.append(ass)
    trust_score.append(ts)
    jas=[] #acne_string
    bas=[] #trust_score

    for i in acne_string:
        for j in i:
            jas.append(j)

    for i in trust_score:
        for j in i:
            bas.append(j)    

    q=0
    w=0
    e=0
    jam=0
    #creating FLAGS for RULES
    for i in jas:
        if i == 'Not_identified':
            jam +=1
            break
        elif i == 'Mild':
            q +=1
        elif i == 'Moderate':
            w +=1
        elif i == 'Severe':
            e +=1

    ex=0
    #final rule set to push
    if q == w == e == jam == 0:
        op = "Please retake the photo with better lighting condition"
        jfk = 0


    elif (q > w) and (q > e) and (q>jam):
        op = 'Mild level Acne Detected'
        jfk = avg(bas)
    elif (w > q) and (w>e) and (w>jam):
        op = 'Moderate level Acne Detected'
        jfk = avg(bas)
    elif (e > w) and (e > q) and (e>jam):
        op = 'Severe Level Acne Detected'
        jfk = avg(bas)
    elif (q == w) or (w == e) or (w == jam):
        op = 'Please retake the image'
        jfk = 0
    else:
        op = 'Not able to determine-please retake the photo'
        jfk = 0

    return json.dumps({"score": jfk, "text": op, "Exceptions": ex}, indent=4)

'''

