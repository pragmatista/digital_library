import face_recognition as fr
import cv2
import numpy as np
import os
import json

'''
https://betterprogramming.pub/step-by-step-face-recognition-in-images-ad0ad302058a
https://data-flair.training/blogs/python-face-recognition/
https://medium.com/an-idea/image-face-recognition-in-python-30b6b815f105
'''

people_model = {
    'model_id': '',
    'folder': 'Kyle',
    'full_path': '',
    'file': '',
    'classification': '',
    'name': ''
}

data = {
    'value1': 2,
    'value2': 2,
    'a_dict_of_values': {
        'd1': 'hello',
        'd2': 'world'
    },
    'value3': 1.234
}


# function to add to JSON
def write_json(new_data, filename='data.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["emp_details"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


write_json(data)

#
#
#
# path = "tests/samples/ml/train/"
# known_names = []
# known_name_encodings = []
#
# images = os.listdir(path)
# for _ in images:
#     image = fr.load_image_file(path + _)
#     image_path = path + _
#     encoding = fr.face_encodings(image)[0]
#
#     known_name_encodings.append(encoding)
#     known_names.append(os.path.splitext(os.path.basename(image_path))[0].capitalize())
#
# print(known_names)
#
# test_image = "tests/samples/ml/test/test2.jpg"
# image = cv2.imread(test_image)
# # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#
# face_locations = fr.face_locations(image)
# face_encodings = fr.face_encodings(image, face_locations)
#
# for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#     matches = fr.compare_faces(known_name_encodings, face_encoding)
#     name = ""
#
#     face_distances = fr.face_distance(known_name_encodings, face_encoding)
#     best_match = np.argmin(face_distances)
#     print(f"Distances: {face_distances}")
#
#     if matches[best_match]:
#         name = known_names[best_match]
#
#     cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 3)
#     cv2.rectangle(image, (left, bottom - 50), (right, bottom), (0, 0, 255), cv2.FILLED)
#     font = cv2.FONT_HERSHEY_DUPLEX
#     cv2.putText(image, name, (left + 6, bottom), font, 2.0, (255, 255, 255), 5)
#
#
# cv2.imshow("Result", image)
# cv2.imwrite("tests/samples/ml/test/output.jpg", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
