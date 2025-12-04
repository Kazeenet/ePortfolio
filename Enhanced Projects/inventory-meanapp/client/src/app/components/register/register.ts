import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

// Angular Material
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';

import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule
  ],
  templateUrl: './register.html',
  styleUrl: './register.css'
})
export class RegisterComponent {

  user = {
    username: '',
    password: '',
    confirmPassword: ''
  };

  constructor(private authService: AuthService, private router: Router) { }

  register() {
    if (this.user.password !== this.user.confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    this.authService.register(
      this.user.username,
      this.user.password
    ).subscribe({
      next: () => {
        alert("Account created! You can now login.");
        this.router.navigate(['/login']);
      },
      error: err => alert(err.error.message || "Registration failed")
    });

  }

  goToLogin() {
    this.router.navigate(['/login']);
  }
}
