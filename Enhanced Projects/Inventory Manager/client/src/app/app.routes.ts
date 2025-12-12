import { Routes } from '@angular/router';
import { ItemListComponent } from './components/item-list/item-list';
import { AddItemComponent } from './components/add-item/add-item';
import { EditItemComponent } from './components/edit-item/edit-item';
import { LoginComponent } from './components/login/login';
import { RegisterComponent } from './components/register/register';
import { AuthGuard } from './guards/auth.guard';


export const routes: Routes = [
  { path: '', component: ItemListComponent, canActivate: [AuthGuard] },
  { path: 'add', component: AddItemComponent, canActivate: [AuthGuard] },
  { path: 'edit/:id', component: EditItemComponent, canActivate: [AuthGuard] },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
];

