# Spec Patch: Bitcoin Payments

Proposes spec updates to satisfy SDD quality rules (adding out-of-scope declarations and test strategies to prevent spec validation failures).

---

```diff
--- phases/examples/failed-spec-example.md
+++ phases/examples/failed-spec-example.md
@@ -8,3 +8,11 @@
 - [ ] User can connect their Coinbase wallet.
 - [ ] The system must process transaction receipts within 5 seconds.
+
+## 3. Non-Goals / Out of Scope
+- Hardware wallet connections (e.g. Ledger, Trezor) will not be supported.
+- Altcoin payments (Ethereum, Litecoin, etc.) are excluded.
+
+## 4. Test Considerations
+- Mock Coinbase API responses in integration test cases.
+- Run simulated network delay tests to verify the 5-second processing timeout boundary.
```
