---
NoteStatus: draft
---

# Gitlab CI 配置

## `variables`

定义的 variables 可以在所有的 job 中使用，可作为环境变量被访问到。

## `needs` vs `dependencies`

* `dependencies`: only says which artifacts your job is going to download, as opposed to the default behavior of jobs, which is to download all artifacts of all preceding jobs.
* `needs`: is about order of execution and creating DAGs. The job will start right away once all the declared jobs complete, irrespective of what stage: is declared. needs: also implies the same effect as dependencies:.

If you use needs:, you don't need to also declare dependencies: (but if you do, they must be the same values). If you don't use needs: the order of job execution is controlled by the stage in which the job is declared.

If you want to use a dependent job just to control ordering but not download its artifacts, use `needs:artifacts:`.

Which one should be used to specify the order of execution and also pulls artifacts

Simply using `needs: [job1, job2, etc]` covers this case.

To break it down:

* To control which dependencies' artifacts are downloaded, without changing order of execution: use `dependencies: [job1, job2]`
* To control order of execution and download artifacts, just use `needs: [job1, job2]`
* To control order of execution, but avoid downloading artifacts, use `needs:artifacts:`

## `artifacts`

如果 artifacts 用在了 release 中，那么不管 expire_in 设置多少，都会一直保留。

## `parallel matrix`

```yaml
test:
  stage: test
  script:
    - echo "Running tests $TEST"
  parallel:
    matrix:
      TEST: ["unit", "integration]
```

TEST 可以在 script 中使用。
