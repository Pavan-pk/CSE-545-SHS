import pickle
import pandas as pd
import numpy
import os
from sklearn.metrics.pairwise import cosine_similarity
from flask import current_app as app
from hms_backend.project_constants import constants


class ChatBot:
    def __init__(self):
        self.path = app.config[constants.ML_PATH]
        self.model = pickle.load(open(os.path.join(self.path, 'chatbot_model.pkl'), 'rb'))

    def get_predict(self, user_type, test):
        COLUMN_NAMES = ['Question', 'Answer']
        DATASET_ENCODING = "ISO-8859-1"
        if user_type == "hospital staff":
            questions_dataset = pd.read_csv(os.path.join(self.path, 'questions_hospital_staff.csv'),
                                            encoding=DATASET_ENCODING, names=COLUMN_NAMES, usecols=['Question'],
                                            header=None)
            answers_dataset = pd.read_csv(os.path.join(self.path, 'questions_hospital_staff.csv'),
                                          encoding=DATASET_ENCODING, names=COLUMN_NAMES, usecols=['Answer'],
                                          header=None)
        elif user_type == "doctor":
            questions_dataset = pd.read_csv(os.path.join(self.path, 'questions_doctors.csv'),
                                            encoding=DATASET_ENCODING, names=COLUMN_NAMES, usecols=['Question'],
                                            header=None)
            answers_dataset = pd.read_csv(os.path.join(self.path, 'questions_doctors.csv'),
                                          encoding=DATASET_ENCODING, names=COLUMN_NAMES, usecols=['Answer'],
                                          header=None)
        elif user_type == "lab staff":
            questions_dataset = pd.read_csv(os.path.join(self.path, 'questions_lab_staff.csv'),
                                            encoding=DATASET_ENCODING, names=COLUMN_NAMES, usecols=['Question'],
                                            header=None)
            answers_dataset = pd.read_csv(os.path.join(self.path, 'questions_lab_staff.csv'),
                                          encoding=DATASET_ENCODING, names=COLUMN_NAMES, usecols=['Answer'],
                                          header=None)
        elif user_type == "insurance staff":
            questions_dataset = pd.read_csv(os.path.join(self.path, 'questions_insurance_staff.csv'),
                                            encoding=DATASET_ENCODING, names=COLUMN_NAMES, usecols=['Question'],
                                            header=None)
            answers_dataset = pd.read_csv(os.path.join(self.path, 'questions_insurance_staff.csv'),
                                          encoding=DATASET_ENCODING, names=COLUMN_NAMES, usecols=['Answer'],
                                          header=None)
        elif user_type == "administrator":
            questions_dataset = pd.read_csv(os.path.join(self.path, 'questions_administrator.csv'),
                                            encoding=DATASET_ENCODING, names=COLUMN_NAMES, usecols=['Question'],
                                            header=None)
            answers_dataset = pd.read_csv(os.path.join(self.path, 'questions_administrator.csv'),
                                          encoding=DATASET_ENCODING, names=COLUMN_NAMES, usecols=['Answer'],
                                          header=None)
        else:
            questions_dataset = pd.read_csv(os.path.join(self.path, 'questions_patients.csv'),
                                            encoding=DATASET_ENCODING, names=COLUMN_NAMES, usecols=['Question'],
                                            header=None)
            answers_dataset = pd.read_csv(os.path.join(self.path, 'questions_patients.csv'),
                                          encoding=DATASET_ENCODING, names=COLUMN_NAMES, usecols=['Answer'],
                                          header=None)
        q1 = questions_dataset.to_numpy()
        q2 = q1.flatten()
        a1 = answers_dataset.to_numpy()
        a2 = a1.flatten()
        questions_dataset.to_numpy()
        embeddings = self.model.encode(q2)
        sentence_embeddings = embeddings
        embeddings_test = self.model.encode(str(test))
        similarity = cosine_similarity([embeddings_test], sentence_embeddings[0:])
        index = numpy.argmax(similarity)
        return a2[index]

    def get_chatbot_reply(self, user, query):
        return self.get_predict(user, query)

