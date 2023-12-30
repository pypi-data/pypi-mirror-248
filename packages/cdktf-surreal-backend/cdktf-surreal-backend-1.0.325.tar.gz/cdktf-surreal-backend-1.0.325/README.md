# cdktf-surreal-backend

This is library to create a CDKTF construct for [terraform-backend-surreal](https://github.com/awlsring/terraform-backend-surreal). This library vends a single construct, `SurrealBackend`, which extends the default `HttpBackend` construct to make instantiation of this easier.

## Usage

### Example

```python
import { TerraformStack } from "cdktf";
import { SurrealBackend } from '@awlsring/cdktf-surreal-backend';

export class MyStack extends TerraformStack {
  constructor(scope: Construct, name: string, props: MyStackProps) {
    super(scope, name);

    const backend = new SurrealBackend(this, 'Backend', {
      address: 'https://localhost:8032',
      project: "homelab",
      stack: "infra",
      username: "terraform",
      password: "alligator3",
    });

    ... // other stuff

  }
}
```

### Construct Properties:

* address: The address your backend sever is reachable at.
* project: The project name to use for this stack.
* stack: The stack name to use for this stack. stacks names must be unique across a project.
* username: The username to use for authentication, configured in the server's config.yaml file
* password: The password to use for authentication, configured in the server's config.yaml file
