---
title: Hello, Quarto Python
date: "2023-12-31"
categories: 
  - Matplotlib
  - Coordinates
format: hugo-md
jupyter: python3
---

<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous" data-relocate-top="true"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


## Quarto

Quarto enables you to weave together content and executable code into a finished document. To learn more about Quarto see <https://quarto.org>.

## Running Code

When you click the **Render** button a document will be generated that includes both content and the output of embedded code. You can embed code like this:

``` python
import pandas as pd
datos = pd.read_csv("ejemplo.csv")
datos.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

|     | Sepal.Length | Sepal.Width | Petal.Length | Petal.Width | Species |
|-----|--------------|-------------|--------------|-------------|---------|
| 0   | 5.1          | 3.5         | 1.4          | 0.2         | setosa  |
| 1   | 4.9          | 3.0         | 1.4          | 0.2         | setosa  |
| 2   | 4.7          | 3.2         | 1.3          | 0.2         | setosa  |
| 3   | 4.6          | 3.1         | 1.5          | 0.2         | setosa  |
| 4   | 5.0          | 3.6         | 1.4          | 0.2         | setosa  |

</div>

You can add options to executable code like this

``` python
2 + 2
```

    4

The `echo: false` option disables the printing of code (only output is displayed).
