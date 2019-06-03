import { TestBed } from '@angular/core/testing';

import { TurflistService } from './turflist.service';

describe('TurflistService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: TurflistService = TestBed.get(TurflistService);
    expect(service).toBeTruthy();
  });
});
