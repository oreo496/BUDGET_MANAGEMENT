# 🎨 Fix White Font Color - Can't See Text

## 🔍 Problem: White text on white background (can't see what you're typing)

---

## ✅ Solution 1: Change Editor Theme (VS Code/Cursor)

### Quick Fix:

1. **Press:** `Ctrl + K` then `Ctrl + T`
   - This opens the theme selector

2. **Choose a light theme:**
   - "Light+" (default light)
   - "Quiet Light"
   - "Solarized Light"
   - Any theme with "Light" in the name

### Or Manual:

1. Click **File** → **Preferences** → **Color Theme**
2. Select a **Light theme** (not Dark)
3. Text will be black/dark on light background

---

## ✅ Solution 2: Change Specific Color Settings

1. **Press:** `Ctrl + ,` (opens Settings)
2. **Search for:** "editor.tokenColorCustomizations"
3. **Click:** "Edit in settings.json"
4. **Add this:**

```json
{
  "editor.tokenColorCustomizations": {
    "textMateRules": [
      {
        "scope": ["source"],
        "settings": {
          "foreground": "#000000"
        }
      }
    ]
  },
  "editor.foreground": "#000000"
}
```

5. **Save** the file

---

## ✅ Solution 3: Change Editor Background

1. **Press:** `Ctrl + ,`
2. **Search:** "workbench.colorCustomizations"
3. **Click:** "Edit in settings.json"
4. **Add:**

```json
{
  "workbench.colorCustomizations": {
    "editor.background": "#FFFFFF",
    "editor.foreground": "#000000"
  }
}
```

---

## ✅ Solution 4: Reset to Default Light Theme

1. **Press:** `Ctrl + Shift + P`
2. **Type:** "Preferences: Color Theme"
3. **Select:** "Light+ (default light)"
4. **Press Enter**

---

## 🎯 Quickest Fix

**Just press:** `Ctrl + K` then `Ctrl + T`

Then select **"Light+"** theme.

**Text will be black, background will be white!** ✅

---

## 📝 For Command Prompt (if that's the issue)

If you mean Command Prompt text color:

1. **Right-click** on Command Prompt title bar
2. **Properties** → **Colors** tab
3. **Change:**
   - Screen Text: Black
   - Screen Background: White
4. **Click OK**

---

## 🎨 If You Want to Change Font Color in the Funder App

If you want to change text colors in the actual application (not editor):

Edit: `frontend/src/app/globals.css`

Add:
```css
body {
  color: #000000; /* Black text */
  background: #ffffff; /* White background */
}
```

---

**The quickest fix: Press `Ctrl + K` then `Ctrl + T` and choose a Light theme!** 🎯

