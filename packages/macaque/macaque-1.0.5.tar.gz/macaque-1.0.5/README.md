## Macaque   
Stability testing tool based on fastbot transformation.
## Local access

```python
from macaque.core import prepare

prepare(udid='192.168.0.119:5555', 
        package='com.panda.app.wid', 
        duration=2, 
        throttle=800,
        whitelist='com.panda.app.wid.panda_main.activity.MainActivity',
        widget='[{"bounds": "0.1,0.87,1,0.95"}]',
        ime=False)
```

## Thanks
https://github.com/bytedance/Fastbot_Android