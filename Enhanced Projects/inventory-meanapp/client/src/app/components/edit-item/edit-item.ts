import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

// Angular Material
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

import { ItemService, Item } from '../../services/item.service';

@Component({
  selector: 'app-edit-item',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule
  ],
  templateUrl: './edit-item.html',
  styleUrl: './edit-item.css'
})
export class EditItemComponent implements OnInit {

  itemId: string | null = null;
  item: Item = { name: '', quantity: 0 };

  constructor(
    private route: ActivatedRoute,
    private itemService: ItemService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.itemId = this.route.snapshot.paramMap.get('id');

    if (this.itemId) {
      this.itemService.getItems().subscribe(items => {
        const found = items.find(i => i._id === this.itemId);
        if (found) {
          this.item = {
            name: found.name,
            quantity: found.quantity
          };
        }
      });
    }
  }

  saveItem() {
    if (!this.itemId) return;

    this.itemService.updateItem(this.itemId, this.item).subscribe({
      next: () => this.router.navigate(['/']),
      error: err => console.error(err)
    });
  }

  goBack() {
    this.router.navigate(['/']);
  }
}
