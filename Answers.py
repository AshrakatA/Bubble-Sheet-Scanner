import cv2
import scanner
answer_ref=cv2.imread("answer_ref.jpg",cv2.COLOR_BGR2GRAY) #reference containg all possible answers
test = cv2.imread("test_sample9.jpg",cv2.COLOR_BGR2GRAY) #test to extract answers from
file = open("extractedAnswers.txt","w+")
#########################################################
#highlight answers from raw images
def prepare(img):
    img,h=scanner.alignImages(img, answer_ref) #deskew image
    img=scanner.resize(img) #resize image to a default size
    img=scanner.answers(img) #show answers as white dots
    return img

#name of each possible answer
def answersTxt():
    gender=["Male","Female"]
    semester=["Fall","Spring","Summer"]
    dept=[ "MCTA","ENVER","ERGY","BLDG","CESS","COMM","MANF",
         "LAAR","MATL","CISE","HAUD"]
    opinion=["Strongly Agree","Agree","Neutral","Disagree","Strongly Disagree"]
    return gender,semester,dept,opinion

#extract answers as string by comparing sample test with the reference
def getAnswers(test,ref):
    gender,semester,dept,opinion=answersTxt()
    count=0
    for i in ref[0:2]: #get gender which is the first 2 circles in reference
        a = i[0]
        at=test[0][0]
        if ((a + 3) >= at >= (a - 3)) : #if answer has same coordinates as reference with tolerance of 3 pixels
            print(gender[count])
            file.write(gender[count]+"\n")
        count+=1
    count=0
    for i in ref[2:5]:  #get semester which is the 2nd, 3rd and 4th circles in reference
        a = i[0]
        at = test[1][0]
        if ((a + 3) >= at >= (a - 3)):
            print(semester[count])
            file.write(semester[count] + "\n")
        count += 1
    count=0
    for i in ref[5:16]: #get department
        a,b = i[0],i[1]
        at,bt = test[2][0],test[2][1]
        if ((a + 3) >= at >= (a - 3)) and ((b + 3) >= bt >= (b - 3)):
            print(dept[count])
            file.write(dept[count] + "\n")
        count += 1
    count =0
    start=16 #index of first opinion in row 1
    end=22 #index last opinion in row 2
    for i in test[3:23]: #get opinion
        at, bt = i[0], i[1]
        for y in ref[start:end]:
            a, b = y[0], y[1]
            if ((a + 3) >= at >= (a - 3)) and ((b + 3) >= bt >= (b - 3)):
                if(at<550): #if x coordinate of the answer is less than 550 pixels, then it must be "strongly agree"
                  # print(opinion[0])
                    count=0
                elif(550<at<570):
                   #print(opinion[1])
                    count=1
                elif(570<at<620):
                   #print(opinion[2])
                    count=2
                elif(620<at<670):
                   # print(opinion[3])
                    count=3
                else:
                  # print(opinion[4])
                    count=4
                start+=5
                end+=5
                #print(opinion[count])
                file.write(opinion[count] + "\n")
                break;

        
###########################################################


test=prepare(test)
answer_ref=prepare(answer_ref)

allAnswers=scanner.countCircles(answer_ref) #get array of circle objects containing all possible answers
testAnswers=scanner.countCircles(test) #get array of circle objects containing sample test answers

getAnswers(testAnswers,allAnswers) #print answers of sample test, having all possible answers coordinates as a reference

file.close()