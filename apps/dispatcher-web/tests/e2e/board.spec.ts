import { test, expect } from '@playwright/test';

test('Board loads and RBAC Zero-Trust toggle works', async ({ page }) => {
  await page.goto('/');

  // Expect title to be present
  await expect(page.locator('text=Know-Task-OS Dispatcher').or(page.locator('text=AI Dispatcher'))).toBeVisible();

  // Check RBAC toggle initial state
  const rbacSelect = page.locator('select');
  await expect(rbacSelect).toHaveValue('Admin');

  // Change role to Junior (Read-Only)
  await rbacSelect.selectOption('Junior');
  await expect(rbacSelect).toHaveValue('Junior');
  
  // Wait to ensure no crashes happen on RBAC context switch
  await page.waitForTimeout(500);
});
