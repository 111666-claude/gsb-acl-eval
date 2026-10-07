# acl-eval

求值 POSIX ACL：属主分支、命名用户、组并集、mask 掩码与 other 兜底，并按条目建索引。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m acleval --sample=mask
python3 -m acleval --sample=owner
python3 -m acleval --sample=groupunion
python3 -m acleval --sample=other
python3 -m acleval --sample=work
```

## 口径

- **属主**：请求者是属主时只看 `user::`，mask 不参与。
- **命名用户**：命中的 `user:名字:` 权限要与 `mask::` 按位与。
- **组**：请求者的组里能命中的 `group::` 与 `group:名字:` 取并集，再与 `mask::` 按位与。
- **兜底**：以上都不命中时用 `other::`。
- **索引**：命名用户与命名组分别建索引。

## 不变量

- 属主分支不受 mask 影响。
- 组分支是命中条目的并集。
- `scanned` 不随条目数乘查询次数放大：八百条查八百次的 `scanned` 不超过 6000。

## 输出契约

`evaluate(acl, uid, owner, groups)` 返回 `rwx` 形式的权限串。场景打印一行 JSON。
`--sample=work` 打印 `{"entries": N, "scanned": N}`。
