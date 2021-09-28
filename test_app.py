import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db
from app import create_app



DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inh5SjYyQmJhc2w4TVduZEF5VzNxZCJ9.eyJpc3MiOiJodHRwczovL2Rldi03MGZuZDJseS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEyZjc3ODJhZjIwY2IwMDZhY2EwODJhIiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNjMyODU1NDAzLCJleHAiOjE2MzI4NjU0MDMsImF6cCI6IkI5REFyZEVDZ1B2Skl3b05GczNGT0hDeU1tZThSRjZRIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.U_4hkoklJEif3MDMatdv56jYN76N7KqYNz1ZocsqKSho88IUF3_OST8t28kO6EpzITJSbIdCOEkvkgb5B2y9MZJMliUUKejyWEyo-xstc7Vsf3CLpJecXQBy4vCwTCRoE49AIsTMrxoPkldyGZt8hFnhllS24YdgFUSEWp8ehN1j-WxGQ1WKvmsJkZn0SZXRaKFDwKXFomgVmI8-qvMaKT11IZneYWlQFOhNrUgj7DUz575gd9503TvjBbp9mITIeGxxtUMAMStxMdui3DWL7GinVCou1H3QW2omi7X6EJ1oYt9-BRQgO5zZiciS0nutOl_AcT-Q3ySr4Y3zYAMyxQ'
ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inh5SjYyQmJhc2w4TVduZEF5VzNxZCJ9.eyJpc3MiOiJodHRwczovL2Rldi03MGZuZDJseS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE1MzY1ZjZmZjg2ZjYwMDZhMzIwYmI1IiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNjMyODU1NjM2LCJleHAiOjE2MzI4NjU2MzYsImF6cCI6IkI5REFyZEVDZ1B2Skl3b05GczNGT0hDeU1tZThSRjZRIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.kupwpxcBR1SJuqVccKu79qMv7E30JjS_x59LgTuhUo7a5eYEhgOgPJQQz8hO4ar2RwUwydlqvrRUqOX6ekHbVyaGkh2CdKlUQF3bzCzQ5b1JBq8aqdzkS9SCD6__9353fcTbStrXNzDUzi57AV85MvM_1gCTTeKYvCV_ODlDLii49z1Xh_wKNwJqk_UJ6hv5nSE52y81zaL0xtfQx3AWI1Rw761B1sSRj_seZQ9qnOawt_-YXBqvawNlNL4uVINKOCihRtfmG8-ujU1VaeDRKF3tp9arhuvOzRCw4GxItB6aEbqP25sGLZv5SE6L-AapxLVltnbhYG5_GdgExhdoPw'
PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inh5SjYyQmJhc2w4TVduZEF5VzNxZCJ9.eyJpc3MiOiJodHRwczovL2Rldi03MGZuZDJseS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDM5MDIzMTIyODYwNDE0MjkzOTkiLCJhdWQiOiJjb2ZmZWUiLCJpYXQiOjE2MzI4NTUwOTIsImV4cCI6MTYzMjg2NTA5MiwiYXpwIjoiQjlEQXJkRUNnUHZKSXdvTkZzM0ZPSEN5TW1lOFJGNlEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.uVXUrno6W9utydMSaRUk6-Zqfi_Z58_ZE6r8DE7oc0beFHvd-ppCGlSvlRmXp15n7j2NnMzG3AqijGWK_HMIdwazVkYrfmHPYF7h5oOHPsi79SA966D8HA9ghFI5fR-jEdDqY9RgzyV061EBXfkV_78xLnfXwg9FdWmfh3LRLkkGLT-zPzrKKRltyFlNsxkOJMdGbz7mTMAjFhsA1noF_yyL0MgdyDC4A4KQKL5CXmQfOT2RleRSAv5ounMmu7MRDHTzYZZwVz6bMC7ZZXdnRLSABSigjIodge59IcDB1PAom5jPUPuyVb_LkMhBYjz5c5zaBYxhARY0WetSHHFTeQ'

CASTING_DIRECTOR={'Authorization': f'Bearer {DIRECTOR_TOKEN}'}
CASTING_ASSISTANT={'Authorization': f'Bearer {ASSISTANT_TOKEN}'}
EXECUTIVE_PRODUCER={'Authorization': f'Bearer {DIRECTOR_TOKEN}'}


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgresql://postgres:1366@localhost:5432/test'
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