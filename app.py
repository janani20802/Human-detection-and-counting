from flask import Flask,render_template,request,Response
import cv2
from persondetection import DetectorAPI
#from videomodule import argsParser
#from camera import Video
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('front.html')

@app.route('/startpage')
def startpg():
    return render_template('startpage.html')

@app.route('/video')
def vidpg():
    return render_template('vidhtml.html')                                                  

@app.route('/image')
def imgpg():
    return render_template('imghtml.html')

@app.route("/prediction",methods=["POST"])
def prediction():
    imgpath=request.files['image']
    imgpath.save("img.jpg")
    max_count1 = 0
    county1 = []
    max1 = []
    avg_acc1_list = []
    max_avg_acc1_list = []
    max_acc1 = 0
    max_avg_acc1 = 0
    odapi = DetectorAPI()
    threshold = 0.7
    image = cv2.imread("img.jpg")
    img = cv2.resize(image, (image.shape[1], image.shape[0]))
    boxes, scores, classes, num = odapi.processFrame(img)
    person = 0
    acc = 0
    for i in range(len(boxes)):
        if classes[i] == 1 and scores[i] > threshold:
           box = boxes[i]
           person += 1
           cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)  # cv2.FILLED #BGR
           cv2.putText(img, f'P{person, round(scores[i], 2)}', (box[1] - 30, box[0] - 8), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                    (0, 0, 255), 1)  # (75,0,130),
           acc += scores[i]
           if (scores[i] > max_acc1):
            max_acc1 = scores[i]
    if (person > max_count1):
        max_count1 = person
    if(person>=1):
        if((acc / person) > max_avg_acc1):
             max_avg_acc1 = (acc / person)


    opc_count = max_count1
    opc_txt = "Overall Person Count:{}".format(opc_count)
    cv2.putText(img, opc_txt, (5, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
   # cv2.imencode(".jpg",img)
    cv2.imshow("Human Detection from Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #cv2.imencode('.jpg',img)
    #yield(b'--image\r\n'b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n')

    #return render_template("prediction.html",data=prediction())
    return render_template("prediction.html",data=prediction())    

@app.route("/cameradetection")
def camera():
    max_count2 = 0
    framex2 = []
    county2 = []
    max2 = []
    avg_acc2_list = []
    max_avg_acc2_list = []
    max_acc2 = 0
    max_avg_acc2 = 0
    video = cv2.VideoCapture(0)
    odapi = DetectorAPI()
    threshold = 0.7

    check, frame = video.read()
    if check == False:
        print('Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided).')

    x2 = 0
    while video.isOpened():
    # check is True if reading was successful
        check, frame = video.read()
        if (check == True):
             img = cv2.resize(frame, (800, 500))
             boxes, scores, classes, num = odapi.processFrame(img)
             person = 0
             acc = 0
             for i in range(len(boxes)):
            # print(boxes)
            # print(scores)
            # print(classes)
            # print(num)
            # print()
                 if classes[i] == 1 and scores[i] > threshold:
                     box = boxes[i]
                     person += 1
                     cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)  # cv2.FILLED
                     cv2.putText(img, f'P{person, round(scores[i], 2)}', (box[1] - 30, box[0] - 8), cv2.FONT_HERSHEY_COMPLEX,
                            0.5, (0, 0, 255), 1)  # (75,0,130),
                     acc += scores[i]
                     if (scores[i] > max_acc2):
                         max_acc2 = scores[i]

             if(person>max_count2):
                max_count2=person            

      
             county2.append(person)
             x2 += 1
             framex2.append(x2)
             if (person >= 1):
                 avg_acc2_list.append(acc / person)
                 if ((acc / person) > max_avg_acc2):
                    max_avg_acc2 = (acc / person)
             else:
                avg_acc2_list.append(acc)


             lpc_count = person
             opc_count = max_count2
             lpc_txt = "Live Person Count: {}".format(lpc_count)
             opc_txt = "Overall Person Count:{}".format(opc_count)
             cv2.putText(img, lpc_txt, (5, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
             cv2.putText(img, opc_txt, (5, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
             cv2.imshow("Human Detection from Video", img)
             key = cv2.waitKey(1)
             if key & 0xFF == ord('q'):
                 break
        else:
           break

    video.release()
    cv2.destroyAllWindows()

    for i in range(len(framex2)):
         max2.append(max_count2)
         max_avg_acc2_list.append(max_avg_acc2)    
    return render_template("campred.html",data1=camera())    

@app.route("/videodetection")
def video():
    #path=request.files['file']
    #path.save("vid.mp4")
    max_count2 = 0
    framex2 = []
    county2 = []
    max2 = []
    avg_acc2_list = []
    max_avg_acc2_list = []
    max_acc2 = 0
    max_avg_acc2 = 0
    #video input
    video = cv2.VideoCapture("test videos/belgiummarch.mp4")
    odapi = DetectorAPI()
    threshold = 0.7

    check, frame = video.read()
    if check == False:
        print('Video Not Found!. Please Enter a Valid Path (Full path of Video Should be Provided).')

    x2 = 0
    while video.isOpened():
    # check is True if reading was successful
        check, frame = video.read()
        if (check == True):
             img = cv2.resize(frame, (800, 500))
             boxes, scores, classes, num = odapi.processFrame(img)
             person = 0
             acc = 0
             for i in range(len(boxes)):
            # print(boxes)
            # print(scores)
            # print(classes)
            # print(num)
            # print()
                 if classes[i] == 1 and scores[i] > threshold:
                     box = boxes[i]
                     person += 1
                     cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)  # cv2.FILLED
                     cv2.putText(img, f'P{person, round(scores[i], 2)}', (box[1] - 30, box[0] - 8), cv2.FONT_HERSHEY_COMPLEX,
                            0.5, (0, 0, 255), 1)  # (75,0,130),
                     acc += scores[i]
                     if (scores[i] > max_acc2):
                         max_acc2 = scores[i]

             if(person>max_count2):
                max_count2=person            

      
             county2.append(person)
             x2 += 1
             framex2.append(x2)
             if (person >= 1):
                 avg_acc2_list.append(acc / person)
                 if ((acc / person) > max_avg_acc2):
                    max_avg_acc2 = (acc / person)
             else:
                avg_acc2_list.append(acc)


             lpc_count = person
             opc_count = max_count2
             lpc_txt = "Live Person Count: {}".format(lpc_count)
             opc_txt = "Overall Person Count:{}".format(opc_count)
             cv2.putText(img, lpc_txt, (5, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
             cv2.putText(img, opc_txt, (5, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
             cv2.imshow("Human Detection from Video", img)
             key = cv2.waitKey(1)
             if key & 0xFF == ord('q'):
                 break
        else:
           break

    video.release()
    cv2.destroyAllWindows()

    for i in range(len(framex2)):
         max2.append(max_count2)
         max_avg_acc2_list.append(max_avg_acc2)
    return render_template("vidprediction.html",data2=video())     


if __name__=='__main__':
    app.run(debug=True)
