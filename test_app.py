import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db
from app import create_app



PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inh5SjYyQmJhc2w4TVduZEF5VzNxZCJ9.eyJpc3MiOiJodHRwczovL2Rldi03MGZuZDJseS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDM5MDIzMTIyODYwNDE0MjkzOTkiLCJhdWQiOiJjb2ZmZWUiLCJpYXQiOjE2MzI5MTc3MzksImV4cCI6MTYzMzAwNDEzOSwiYXpwIjoiQjlEQXJkRUNnUHZKSXdvTkZzM0ZPSEN5TW1lOFJGNlEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.Vfcu0or8oyxrafl6QyVBli77dyAAAVaC92PBXvkGSVBmrxul66Xyh6mrHrd6ndwLwgk1EqOuCjPSnO7gIM8B82gt4SgBYqt0diZrZT51n4eKfsg1IcBPp8LK9Lsd1Usy3nSzbM_rbEARKNzja5XruBABLK12G8OL9cTub1ivWq6x2-URKD-qtYEZ9xEMsY9Je0H62YvsarIXqTFKxSeGJDNNb8o2VfFMdvr0ahmy2ap9ODK-ONVQxlXcxeJsNBofw7a4FfwAKBKRfHLBFls5y5Fl2x3w8ZwfWd-c0WsOe5tGgRLmzb0XQfNoQD-mV8N4_OuKb5tfCXZlVZdY0ZUG_w'
ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inh5SjYyQmJhc2w4TVduZEF5VzNxZCJ9.eyJpc3MiOiJodHRwczovL2Rldi03MGZuZDJseS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE1MzY1ZjZmZjg2ZjYwMDZhMzIwYmI1IiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNjMyOTE3NTk2LCJleHAiOjE2MzMwMDM5OTYsImF6cCI6IkI5REFyZEVDZ1B2Skl3b05GczNGT0hDeU1tZThSRjZRIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.XirF_Q8zsisXgtf7hNPSb4sQ2IsWrjHCIiE7MEkYihE3OTwABKpwRw_L275IcejTBqgcaFP9lS5vvbCnc0m1ZAbL6jsekwfkkoq6fp-GaQa_MVyubqlg9_y7MvrRUVh_gAnhxqHbh8gEyec6w-rihGznusfmE8Is4GJvF7HdiuINqDkULD68ODL42j7Sqqd5BPkqfJ7MrQAwpnowcECC58JPandeDfsYU1hu_P2KsQnDaR9pnNx5Iztt3lUymJ8x-PJggvFWUGpm0iVST18PzRUcIZfripYIq7DTI90CDYoLlUfxG8hViwCl3D4mKUpHj4T0gCVUExL599BdWNcW6w'
DIRECTOR_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inh5SjYyQmJhc2w4TVduZEF5VzNxZCJ9.eyJpc3MiOiJodHRwczovL2Rldi03MGZuZDJseS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEyZjc3ODJhZjIwY2IwMDZhY2EwODJhIiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNjMyOTE3NDkyLCJleHAiOjE2MzMwMDM4OTIsImF6cCI6IkI5REFyZEVDZ1B2Skl3b05GczNGT0hDeU1tZThSRjZRIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.fT7YTnil1uzWtic45tQwGnCMcCi5zz5oFtTaviHqfAkF_LoNBGrbrI-cR5HVsKEXWJR1_9I1agnwKRSrbIqAxjPO0SBMK3OHqr7rFaqSkYjQluRIBQVJ_vwhrsNnvIWBWc5PDtC7w4dXCDXaBG4_hYznTlmGnBY3XdFQft7E8Swz5qV-DoascBWjUxNw7V0nvd-f5x4UhwTq501pcBQ41katlnDqORVkSEeJKNBkC6dDLyMYyBEPwOBHPeEGyM3_DpzAsU8g5PvS8Q1NuxrFyzL1nr0QOaZul5hamnGHfu2wit7MWoyW5xtzqIsn83tFhDikwXPH4yQXA-6j9uVzrQ"

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
        res = self.client().post('/movies', json=self.movie, headers=EXECUTIVE_PRODUCER)
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
        res = self.client().post('/movies', json={}, headers=EXECUTIVE_PRODUCER)
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
        res = self.client().delete('/movies/2', headers=EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], '2')

    def test_delete_movie_404(self):
        res = self.client().delete('/movies/2134', headers=EXECUTIVE_PRODUCER)
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