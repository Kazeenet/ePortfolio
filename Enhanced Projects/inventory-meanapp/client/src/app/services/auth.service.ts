import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private baseUrl = 'http://localhost:5000/api';  // <-- Option A

  constructor(private http: HttpClient) { }

  // REGISTER
  register(username: string, password: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/auth/register`, { username, password });
  }

  // LOGIN
  login(username: string, password: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/auth/login`, { username, password });
  }

  // LOGOUT
  logout() {
    localStorage.removeItem('token');
  }

  // TOKEN HANDLING
  saveToken(token: string) {
    localStorage.setItem('token', token);
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }
}
