# Config

## Global Config Object

```python
import pykabutan as pk

config = pk.config
```

The global `config` object controls HTTP request behavior.

---

## Properties

### `timeout`

```python
@property
def timeout(self) -> int

@timeout.setter
def timeout(self, value: int | float) -> None
```

HTTP request timeout in seconds.

**Default:** `30`

**Validation:** Must be positive (> 0)

**Example:**

```python
pk.config.timeout = 60
print(pk.config.timeout)  # 60
```

---

### `request_delay`

```python
@property
def request_delay(self) -> float

@request_delay.setter
def request_delay(self, value: int | float) -> None
```

Delay between consecutive HTTP requests in seconds.

**Default:** `0.5`

**Validation:** Must be non-negative (>= 0)

**Example:**

```python
pk.config.request_delay = 1.0
print(pk.config.request_delay)  # 1.0
```

---

### `user_agent`

```python
@property
def user_agent(self) -> str

@user_agent.setter
def user_agent(self, value: str) -> None
```

HTTP User-Agent header.

**Default:** Chrome browser user agent string

**Validation:** Must be non-empty string

**Example:**

```python
pk.config.user_agent = "MyApp/1.0"
```

---

## Methods

### `reset()`

```python
def reset(self) -> None
```

Reset all configuration to default values.

**Example:**

```python
pk.config.timeout = 120
pk.config.request_delay = 5.0
pk.config.reset()

print(pk.config.timeout)        # 30
print(pk.config.request_delay)  # 0.5
```

---

## Validation Errors

Invalid values raise `ValueError`:

```python
# Timeout must be positive
pk.config.timeout = 0     # ValueError
pk.config.timeout = -1    # ValueError

# Request delay must be non-negative
pk.config.request_delay = -1  # ValueError

# User agent must be non-empty
pk.config.user_agent = ""     # ValueError
pk.config.user_agent = None   # ValueError
```

---

## Type Conversion

Values are automatically converted:

| Input Type | Property | Result |
|------------|----------|--------|
| `float` | `timeout` | Converted to `int` |
| `int` | `request_delay` | Converted to `float` |

```python
pk.config.timeout = 30.7
print(pk.config.timeout)  # 30 (int)

pk.config.request_delay = 2
print(pk.config.request_delay)  # 2.0 (float)
```

---

## Default Values Summary

| Property | Default | Type |
|----------|---------|------|
| `timeout` | `30` | `int` |
| `request_delay` | `0.5` | `float` |
| `user_agent` | Chrome UA | `str` |
