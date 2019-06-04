import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule, MatIconModule,
    MatInputModule, MatListModule, MatMenuModule,
    MatSidenavModule,
    MatTableModule,
    MatTabsModule, MatToolbarModule
} from '@angular/material';

@NgModule({
  declarations: [],
  imports: [
    CommonModule
  ],
    exports: [
        MatTableModule,
        MatCardModule,
        MatInputModule,
        MatFormFieldModule,
        MatButtonModule,
        MatTabsModule,
        MatSidenavModule,
        MatToolbarModule,
        MatIconModule,
        MatListModule,
        MatMenuModule,
    ]
})
export class MaterialModule { }
