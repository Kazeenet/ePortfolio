import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

// Angular Material
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

import { ItemService, Item } from '../../services/item.service';

@Component({
  selector: 'app-add-item',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule
  ],
  templateUrl: './add-item.html',
  styleUrl: './add-item.css'
})
export class AddItemComponent {

  item: Item = {
    name: '',
    quantity: 0
  };

  constructor(
    private router: Router,
    private itemService: ItemService
  ) { }

  submitItem() {
    this.itemService.addItem(this.item).subscribe({
      next: () => this.router.navigate(['/']),
      error: (err) => console.error(err)
    });
  }

  goBack() {
    this.router.navigate(['/']);
  }
}
