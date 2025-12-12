import { Component, OnInit, ChangeDetectorRef, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

// Angular Material imports
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';

import { ItemService, Item } from '../../services/item.service';

@Component({
  selector: 'app-item-list',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [
    CommonModule,
    MatButtonModule,
    MatTableModule,
    MatListModule,
    MatIconModule
  ],
  templateUrl: './item-list.html',
  styleUrl: './item-list.css'
})
export class ItemListComponent implements OnInit {

  items: Item[] = [];
  displayedColumns: string[] = ['name', 'quantity', 'actions'];

  constructor(
    private itemService: ItemService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    this.loadItems();
  }

  loadItems() {
    console.log('Loading items...');

    this.itemService.getItems().subscribe({
      next: (data) => {
        console.log('Items received:', data);
        this.items = data;
        this.cdr.markForCheck();  // 🔥 FIXES ExpressionChangedAfterItHasBeenCheckedError
      },
      error: (err) => console.error('API Error:', err)
    });
  }

  deleteItem(id: string | undefined) {
    if (!id) return;

    this.itemService.deleteItem(id).subscribe(() => {
      this.loadItems(); // refresh table
    });
  }

  editItem(id: string | undefined) {
    if (!id) return;
    this.router.navigate(['/edit', id]);
  }

  goToAdd() {
    this.router.navigate(['/add']);
  }
}
