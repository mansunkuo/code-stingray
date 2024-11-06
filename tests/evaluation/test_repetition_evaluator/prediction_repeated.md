```diff
--- a/.github/workflows/release.yml
+++ b/.github/workflows/release.yml
@@ -25,5 +25,5 @@
           git config user.email "$GITHUB_ACTOR@users.noreply.github.com"
 
       - name: Run chart-releaser
-        uses: helm/chart-releaser-action@v1.6.0
+        uses: helm/chart-releaser-action@v1.8.0
         env:
           CR_TOKEN: "${{ secrets.GITHUB_TOKEN }}"

```