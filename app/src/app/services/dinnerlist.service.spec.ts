import { TestBed } from '@angular/core/testing';

import { DinnerlistService } from './dinnerlist.service';

describe('DinnerlistService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: DinnerlistService = TestBed.get(DinnerlistService);
    expect(service).toBeTruthy();
  });
});
