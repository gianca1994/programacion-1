import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DeleteSensorComponent } from './delete-sensor.component';

describe('DeleteSensorComponent', () => {
  let component: DeleteSensorComponent;
  let fixture: ComponentFixture<DeleteSensorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DeleteSensorComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DeleteSensorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
