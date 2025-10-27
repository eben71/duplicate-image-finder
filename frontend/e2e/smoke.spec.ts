import { test, expect } from '@playwright/test';

test('home page shows duplicate image finder heading', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: /duplicate image finder/i })).toBeVisible();
});
