import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db
from app import create_app



DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inh5SjYyQmJhc2w4TVduZEF5VzNxZCJ9.eyJpc3MiOiJodHRwczovL2Rldi03MGZuZDJseS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDM5MDIzMTIyODYwNDE0MjkzOTkiLCJhdWQiOiJjb2ZmZWUiLCJpYXQiOjE2MzI4OTU0NTIsImV4cCI6MTYzMjkwNTQ1MiwiYXpwIjoiQjlEQXJkRUNnUHZKSXdvTkZzM0ZPSEN5TW1lOFJGNlEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.EYL_IwYZrKLPbTDZhgOgDwECMWwtW-Foi0VAl_xvlfanZN0-vst-12FYpB_D4i49vQRyeYdGkIm3gGw-9hVAqBwDhe6WcSNDj9MhJqXvAI8P_HQnVcjBTr5qGaEPNGNFdv03rlxcHyt51I7TR1BSY_vvYy9FazKLZTzcjmHAts7pdboINd9hNxS8duA9TZ2PFge5LiAAZKim5kygmTm7PnhpBl5b6sFy2rd1IMR5jBBYhjkXaIKOHNinzrJEhw-kHdxPHZSkLpsDKqRVXJFEZj5WyXmqvgEkzjLtGp6obdlTOMbL3rvJ-keHMHWWWFYmCttwLEjYgN3Vk2zssDi1IA'
ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inh5SjYyQmJhc2w4TVduZEF5VzNxZCJ9.eyJpc3MiOiJodHRwczovL2Rldi03MGZuZDJseS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE1MzY1ZjZmZjg2ZjYwMDZhMzIwYmI1IiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNjMyODk0ODM5LCJleHAiOjE2MzI5MDQ4MzksImF6cCI6IkI5REFyZEVDZ1B2Skl3b05GczNGT0hDeU1tZThSRjZRIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.RRNtsfrxlhlwPNV1niQuRjPksvClV9whynDo0nJGDvWNAUCCGtsfhtwPSJoqAKdCAS1zyO8NmT2n4YJZWtUEOWcnh4V4dfgR7SHY6RNdJookXI1uWlnMz6NlnEZAmX8pYtHR8jdE16WwMBe-fl9CquaRCo1znpEXIb6nNZxBLQyFu9SXJWGq9UL1p5_Ik0QRgYaNo3USX96RHilz3W9D5-zKcJbqcLniSXb7Upn3yI6XuSHPihv8TJK7SPQuzG-g487h7OPsuUCIQ5HcMH_hwera1eLd-lwe08OGVIOoPSQCVdd8O1ryjuIXHN-Eh29Tp2ZrxXUi1ye4U8sybXdPig'
PRODUCER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inh5SjYyQmJhc2w4TVduZEF5VzNxZCJ9.eyJpc3MiOiJodHRwczovL2Rldi03MGZuZDJseS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEyZjc3ODJhZjIwY2IwMDZhY2EwODJhIiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNjMyODk2MTMyLCJleHAiOjE2MzI5MDYxMzIsImF6cCI6IkI5REFyZEVDZ1B2Skl3b05GczNGT0hDeU1tZThSRjZRIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.kyGSgds5b32Iw4voLKx302Ca6EpUgMJZCx4-vPISYfk6HJ0m5g1pyVTuc7tuWix3J78i3nG8gzNTc8lsdO1HjgtojyE9o_KmYKVcPAjK7kkMZ8K6xNiZcmd5gcfC2_qF-odAdgbbaehgZHVe0iOY_9dtAJcrRhQF0072DkpiZ_-W9DVBuS3XU4d-BUcBl88xU-wF4AVgMdgqXOTbDq2I-0-y6AadDA-wNIZhXVc0yVpoPzKl8oNjNwMDzy8UFEi0nljWYeh43xUPVikz9cYtUrM1xsQZZTIduyjxz7MxD8YvFHXjf3_SuyJGEDmFB_KhcCHbxhEYR022qn-dCydwjA"

CASTING_DIRECTOR={'Authorization': f'Bearer {DIRECTOR_TOKEN}'}
CASTING_ASSISTANT={'Authorization': f'Bearer {ASSISTANT_TOKEN}'}
EXECUTIVE_PRODUCER={'Authorization': f'Bearer {PRODUCER_TOKEN}'}

#https://dev-70fnd2ly.us.auth0.com/authorize?audience=coffee&response_type=token&client_id=B9DArdECgPvJIwoNFs3FOHCyMme8RF6Q&redirect_uri=http://127.0.0.1:5000/

class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.getenv('DATABASE_URL')
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
        res = self.client().post('/actors', json={}, headers=CASTING_DIRECTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
    


    def test_patch_actor_200(self):
        res = self.client().patch('/actors/1', json=self.actor, headers=EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_patch_actor_400(self):
        res = self.client().patch('/actors/1', json={}, headers=EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_patch_actor_401(self):
        res = self.client().patch('actors/1', json=self.actor, headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_actor_200(self):
        res = self.client().delete('/actors/2', headers=EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], '2')



    def test_delete_actor_404(self):
        res = self.client().delete('/actors/1000', headers=EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_actor_401(self):
        res = self.client().delete('/actors/2', headers='')
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
        res = self.client().post('/movies', json={}, headers=CASTING_DIRECTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_patch_movie(self):
        res = self.client().patch('/movies/1', json=self.movie, headers=EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movie_400(self):
        res = self.client().patch('/movies/1', json={}, headers=EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_patch_movie_401(self):
        res = self.client().patch('movies/1', json=self.movie, headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
    
    def test_delete_movie(self):
        res = self.client().delete('/movies/2', headers=CASTING_DIRECTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], '2')

    def test_delete_movie_404(self):
        res = self.client().delete('/movies/2134', headers=CASTING_DIRECTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movie_401(self):
        res = self.client().delete('/movies/2', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


if __name__ == '__main__':
    unittest.main()