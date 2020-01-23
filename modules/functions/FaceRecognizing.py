import face_recognition

def compareFaces(knownImageUrl, unknownImageUrl):
    knownImage = face_recognition.load_image_file(knownImageUrl)
    unknownImage = face_recognition.load_image_file(unknownImageUrl)
    knownEncoding = face_recognition.face_encodings(knownImage)[0]
    unknownEncoding = face_recognition.face_encodings(unknownImage)[0]
    return face_recognition.compare_faces([knownEncoding], unknownEncoding)


if __name__ == '__main__':
    img1 = 'C:\\Users\\wpadala\\PycharmProjects\\PersonDataSearcher\\modules\\functions\\pobrane.jpg'
    img2 = 'C:\\Users\\wpadala\\PycharmProjects\\PersonDataSearcher\\modules\\functions\\pobrane (2).jpg'
    print(compareFaces(img1,img2))
