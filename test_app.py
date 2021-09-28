import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db
from app import create_app



DIRECTOR_TOKEN = ''
ASSISTANT_TOKEN = ''
PRODUCER_TOKEN = ''

CASTING_DIRECTOR={'Authorization': f'Bearer {DIRECTOR_TOKEN}'}
CASTING_ASSISTANT={'Authorization': f'Bearer {ASSISTANT_TOKEN}'}
EXECUTIVE_PRODUCER={'Authorization': f'Bearer {DIRECTOR_TOKEN}'}


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)

        self.movie = {
            'title': 'John Wick',
            'release_date': '1979-02-09'
        }

        self.actor = {
            'name': 'claire everly',
            'age': 44,
            'gender': 'Female'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

        # actors 

    def test_get_actors_200(self):
        res = self.client().get('/actors', headers=CASTING_ASSISTANT)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_actors_401(self):
        res = self.client().get('/actors', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertFalse(len(data['movies']))

    def test_post_actor_201(self):
        res = self.client().post('/actors', json=self.actor, headers=CASTING_DIRECTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_post_actor_401(self):
        res = self.client().post('/actors', json=self.actor, headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_post_actor_400(self):
        res = self.client().post('/actors', json='', headers=CASTING_DIRECTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request, Wrong input')

    def test_patch_actor_200(self):
        res = self.client().patch('/actors/1', json=self.actor, headers=EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_patch_actor_400(self):
        res = self.client().patch('/actors/1', json='', headers=EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_patch_actor_401(self):
        res = self.client().patch('actors/1', json=self.actor, headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_actor_200(self):
        res = self.client().delete('/actors/1', headers=EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_delete_actor_404(self):
        res = self.client().delete('/actors/1000', headers=EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_actor_401(self):
        res = self.client().delete('/actors/1', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


        #movies

    def test_get_movies(self):
        res = self.client().get('/movies', headers=CASTING_ASSISTANT)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_get_movies_401(self):
        res = self.client().get('/movies', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertFalse(len(data['movies']))

    def test_post_movie(self):
        res = self.client().post('/movies', json=self.movie, headers=CASTING_DIRECTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_post_movie_401(self):
        res = self.client().post('/movies', json=self.movie, headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_post_movie_400(self):
        res = self.client().post('/movies', json='', headers=CASTING_DIRECTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request, Worng input')

    def test_patch_movie(self):
        res = self.client().patch('/movies/1', json=self.movie, headers=PRODUCER_TOKEN)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_patch_movie_400(self):
        res = self.client().patch('/movies/1', json='', headers=PRODUCER_TOKEN)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_patch_movie_401(self):
        res = self.client().patch('movies/1', json=self.movie, headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers=PRODUCER_TOKEN)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_delete_movie_404(self):
        res = self.client().delete('/movies/2134', headers=PRODUCER_TOKEN)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movie_401(self):
        res = self.client().delete('/movies/1', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)



if __name__ == '__main__':
    unittest.main()