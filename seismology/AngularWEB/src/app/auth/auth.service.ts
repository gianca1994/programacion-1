import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { API_URL } from '../env';
import jwt_decode from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  token;

  constructor(private http: HttpClient, private router: Router) { }

  public get isAuthenticated(): boolean {
    return (localStorage.getItem('token') !== null);}

  public get isAdmin(): boolean {
    if (localStorage.getItem('token') !== null) {
      const token_decode = jwt_decode(localStorage.getItem('token'));
      if (token_decode.user_claims.admin) {return true;}};
  }

  login(email: string, password: string) {
    this.http.post(API_URL + '/auth/login', { email: email, password: password }).subscribe((resp: any) => {
      this.router.navigate(['']);
      localStorage.setItem('token', resp.access_token);
    })
  }

  logout() {
    localStorage.removeItem('token');
    this.router.navigate(['login']);
  }
}
