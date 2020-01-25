import face_recognition


def compare_faces(known_image_url, unknown_image_url):
    known_image = face_recognition.load_image_file(known_image_url)
    unknown_image = face_recognition.load_image_file(unknown_image_url)
    known_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    for result in face_recognition.compare_faces([known_encoding], unknown_encoding):
        if str(result) is 'True':
            return True
    return False


if __name__ == '__main__':
    img1 = 'C:\\Users\\wpadala\\PycharmProjects\\PersonDataSearcher\\modules\\functions\\pobrane (5).jpg'
    img2 = 'C:\\Users\\wpadala\\PycharmProjects\\PersonDataSearcher\\modules\\functions\\images.jpg'
    print(compare_faces(img1, img2))


