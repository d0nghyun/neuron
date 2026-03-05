.hooks as $orig |
.hooks = (
  $orig | to_entries | map(
    .key as $event |
    .value = [
      .value[] |
      . as $group |
      if ($group.hooks | type) == "array" then
        $group | .hooks = [$group.hooks[] | select((.command // "") | contains("[module:") | not)]
      else $group end
    ] |
    .value = [.value[] | select((.hooks | length) > 0)]
  ) | from_entries
)
