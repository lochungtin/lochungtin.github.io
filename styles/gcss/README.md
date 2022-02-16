# GCSS

Short for Global CSS - this is a simple css file consists of class primarily used for layout styling with flex.

Made to simply save some lines of code and a bit of your time write layout css again and again.

## Usage

### Cloning

First clone the repo
```bash
git clone https://github.com/lochungtin/gccs.git
```

Then import the stylesheet file as you would normal import any other css file

### Linking

```html
<link rel='stylesheet' href='https://raw.githubusercontent.com/lochungtin/gcss/master/layout.css'>
```

## Class naming

Class names are systematically named, which is in the format of 
```
{ row / col }-{ left / spread / right }-{ top / center / bottom }
```

`row / col`: corresponds to the attribute flex-direction

`left / spread / right`: corresponds to the attribute justify-content
 - left = flex-start
 - spread = space-between
 - right = flex-end

`top / center / bottom`: corresponds to the attribute align-items
 - top = flex-start
 - center = center
 - bottom = flex-end

### Exception

`absCenter` is the class that centers everything, both `align-items` and `justify-content`

### Full list
- .absCenter
- row classes
  - .row-left-top
  - .row-left-center
  - .row-left-bottom
  - .row-spread-top
  - .row-spread-center
  - .row-spread-bottom
  - .row-right-top
  - .row-right-center
  - .row-right-bottom
- column classes
  - .col-left-top
  - .col-left-center
  - .col-left-bottom
  - .col-spread-top
  - .col-spread-center
  - .col-spread-bottom
  - .col-right-top
  - .col-right-center
  - .col-right-bottom
